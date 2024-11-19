import datetime
import json
import os

import pandas as pd
import joblib
from loguru import logger

from backend.app.event_manager.manager_kafka import ManagerKafka
from backend.app.tasks.xg_boost_ml.schemas import DepositSchema


class CalculateDepositManager:

    def __init__(self):
        self.model_path: str = 'backend/ml_models/xgboost_model.joblib'
        if os.path.exists(self.model_path):
            print(f"File found at: {os.path.abspath(self.model_path)}")
        else:
            print(f"File not found at: {os.path.abspath(self.model_path)}")

        self.education_value_default: str = 'среднее'
        self.occupation_value_default: str = 'самозанятый'

    async def run(self):
        async with ManagerKafka().consumer as consumer:
            async for data_row in consumer.consumption():
                date_now: datetime.date = datetime.date.today()
                data_profile: dict = json.loads(data_row['value'])
                deposit_schema: DepositSchema = DepositSchema(**{
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
                deposit = self.calculate(deposit_schema)
                logger.info({
                    'user_id': data_profile['user_id'],
                    'deposit': deposit,
                    'rate_date': f'{date_now.year}.{date_now.month}'
                })

    def calculate(self, deposit_schema: DepositSchema):
        logger.info('calculate start')
        loaded_model = self.load_model(self.model_path)
        logger.info('loaded_model complete')

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
            'married': [deposit_schema.married],
            'year': [deposit_schema.year],
            'month': [deposit_schema.month]
        })
        predicted_savings = loaded_model.predict(new_data)
        logger.info('predicted_savings complete')

        return predicted_savings[0]

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
