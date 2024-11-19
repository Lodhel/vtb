import datetime
import json

import pandas as pd
import joblib
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.event_manager.manager_kafka import ManagerKafka
from backend.app.models import RecommendedDeposit
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.tasks.xg_boost_ml.schemas import DepositSchema, RecommendedDepositSchema


class CalculateDepositManager(ManagerSQLAlchemy):

    def __init__(self):
        model_path: str = 'backend/ml_models/xgboost_model_1_4_2.joblib'
        self.xgboost_model = self.load_model(model_path)

        self.education_value_default: str = 'среднее'
        self.occupation_value_default: str = 'самозанятый'

    async def run(self):
        async with ManagerKafka().consumer as consumer:
            async for data_row in consumer.consumption():
                date_now: datetime.date = datetime.date.today()
                data_profile: dict = json.loads(data_row['value'])
                logger.info(data_profile)
                deposit_schema: DepositSchema = self.create_deposit_schema(data_profile, date_now)
                deposit: float = self.calculate(deposit_schema)
                rate_date: datetime.date = datetime.datetime.strptime(f'{date_now.year}-{date_now.month}', "%Y-%m").date()

                await self.save_recommended_deposit(
                    RecommendedDepositSchema(**{
                        'user_id': data_profile['user_id'],
                        'deposit': deposit,
                        'rate_date': rate_date
                    })
                )

    async def save_recommended_deposit(self, recommended_deposit_schema: RecommendedDepositSchema):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            recommended_deposit_query = await session.execute(
                select(
                    RecommendedDeposit
                ).filter_by(
                    user_id=recommended_deposit_schema.user_id,
                    rate_date=recommended_deposit_schema.rate_date
                )
            )
            recommended_deposit: RecommendedDeposit | None = recommended_deposit_query.scalars().first()

            if recommended_deposit:
                recommended_deposit.deposit = recommended_deposit_schema.deposit
            else:
                recommended_deposit: RecommendedDeposit = RecommendedDeposit(
                    user_id=recommended_deposit_schema.user_id,
                    rate_date=recommended_deposit_schema.rate_date,
                    deposit=recommended_deposit_schema.deposit
                )
                session.add(recommended_deposit)

            await session.commit()

    @staticmethod
    def create_deposit_schema(data_profile: dict, date_now: datetime.date):
        return DepositSchema(**{
            'income': data_profile['income_last_month'],
            'expense': data_profile['expenses_last_month'],
            'count_child': data_profile['children_count'],
            'curs_dollar': 86,
            'curs_euro': 94,
            'curs_uan': 12,
            'oil_brent': 70,
            'rate': 5,
            'inf': 3,
            'education': data_profile['education'],
            'work': data_profile['occupation'],
            'married': data_profile['marital_status'],
            'year': date_now.year,
            'month': date_now.month
        })

    def calculate(self, deposit_schema: DepositSchema) -> float:
        base_logic_result: float = self.calculate_base_logic(deposit_schema)
        xgboost_result: float = self.calculate_at_xgboost(deposit_schema)

        return round(
            (base_logic_result + xgboost_result) / 2,
            2
        )

    def calculate_base_logic(self, deposit_schema: DepositSchema) -> float:
        disposable_income: int = deposit_schema.income - deposit_schema.expense
        savings_rate: float = self._get_savings_rate(deposit_schema)
        predicted_savings: float = disposable_income * savings_rate

        return predicted_savings

    def calculate_at_xgboost(self, deposit_schema: DepositSchema) -> float:
        new_data = pd.DataFrame({
            'income': [deposit_schema.income],
            'expense': [deposit_schema.expense],
            'count_child': [deposit_schema.count_child],
            'curs_dollar': [deposit_schema.curs_dollar],
            'curs_euro': [deposit_schema.curs_euro],
            'curs_uan': [deposit_schema.curs_uan],
            'oil_brent': [deposit_schema.oil_brent],
            'rate': [deposit_schema.rate],
            'inf': [deposit_schema.inf],
            'education': [deposit_schema.education],
            'work': [deposit_schema.work],
            'married': ['женат' if deposit_schema.married else 'не женат'],
            'year': [deposit_schema.year],
            'month': [deposit_schema.month]
        })
        predicted_savings = self.xgboost_model.predict(new_data)

        return float(predicted_savings[0])

    @staticmethod
    def _get_savings_rate(deposit_schema: DepositSchema) -> float:
        # Устанавливаем базовый коэффициент сбережений
        base_rate = 0.2

        # Корректируем коэффициент на основе количества детей
        if deposit_schema.count_child > 0:
            base_rate -= 0.03 * deposit_schema.count_child  # Каждый ребенок -> уменьшаем депозит

        # Учитываем влияние инфляции
        base_rate -= 0.01 * (deposit_schema.inf / 100)

        # Учитываем уровень образования (пример категориального признака)
        if deposit_schema.education.lower() in ["higher", "university"]:
            base_rate += 0.05

        # Учитываем семейное положение
        if deposit_schema.married:
            base_rate += 0.03  # Увеличиваем коэффициент для женатых/замужних

        # Ограничиваем коэффициент в разумных пределах
        base_rate = max(0.05, min(0.4, base_rate))
        return base_rate

    @staticmethod
    def load_model(model_path):
        return joblib.load(model_path)

    def convert_profile_education(self, target: str):
        education_converter: dict = {
            'MIDDLE': 'среднее',
            'HIGHER': 'высшее',
            'POSTGRADUATE': 'послевузовское',
        }
        return education_converter.get(target, self.education_value_default)

    def convert_profile_occupation(self, target: str):
        occupation_converter: dict = {
            'SELF_EMPLOYED': 'самозанятый',
            'GOVERNMENT_EMPLOYEE': 'госслужащий',
            'PRIVATE_COMPANY_EMPLOYEE': 'работник частной компании',
        }
        return occupation_converter.get(target, self.education_value_default)
