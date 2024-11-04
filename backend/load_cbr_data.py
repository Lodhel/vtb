import asyncio
import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import InflationGoal, KeyRate, InterbankRate, CurrencyRate, MetalPrice, Reserve, \
    BankRequirement, InflationData
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.cbr.cbr_extend_parser import CBR_ExtendParser
from backend.cbr.cbr_parser import CBRParser


class CBR_Loader(CBRParser, CBR_ExtendParser):

    def __init__(self):
        super(CBR_Loader, self).__init__()
        self.data: dict = {}

    async def load(self):
        await self.parse_extend_page()
        await self.parse_main_page()

    async def parse_extend_page(self) -> None:
        soup = await self.fetch_content(self.BASE_EXTEND_URL)
        if soup:
            self.data['inflation'] = self.parse_inflation(soup)
            self.data['key_rate'] = self.parse_key_rate(soup)
            self.data['interbank_rates'] = self.parse_interbank_rates(soup)
            self.data['currency_rates'] = self.parse_currency_rates(soup)
            self.data['metal_prices'] = self.parse_metal_prices(soup)
            self.data['reserves'] = self.parse_reserves(soup)
            self.data['liquidity_indicators'] = self.parse_liquidity_indicators(soup)
            self.data['bank_requirements'] = self.parse_bank_requirements(soup)

    async def parse_main_page(self) -> None:
        soup = await self.fetch_content(self.BASE_URL)
        if soup:
            self.data['inflation_backup'] = self.parse_inflation_backup(soup)
            self.data['key_rate_backup'] = self.parse_key_rate_backup(soup)
            self.data['ruonia_rate'] = self.parse_ruonia_rate(soup)
            self.data['currency_rates_backup'] = self.parse_currency_rates_backup(soup)


class CBR_DB_Manager(ManagerSQLAlchemy, CBR_Loader):

    def __init__(self):
        super(CBR_DB_Manager, self).__init__()
        self.is_date: datetime.date = datetime.date.today()

    async def run(self):
        await self.load()
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            await self.save_data(session)

    async def save_data(self, session: AsyncSession):
        await self.save_inflation(session)
        await self.save_key_rate(session)
        await self.save_interbank_rates(session)
        await self.save_currency_rates(session)
        await self.save_metal_prices(session)
        await self.save_reserve(session)
        await self.save_bank_requirements(session)

    async def save_inflation(self, session: AsyncSession):
        await self.save_inflation_goal(session)
        await self.save_inflation_data(session)

    async def save_inflation_goal(self, session: AsyncSession):
        inflation_goal = InflationGoal(
            is_date=self.is_date,
            rate_value=self.data['inflation']['inflation_goals']
        )
        session.add(inflation_goal)
        await session.flush()

    async def save_inflation_data(self, session: AsyncSession):
        inflation_goal = InflationData(
            is_date=self.is_date,
            rate_value=self.data['inflation']['inflation_data']['rate_value'],
            rate_change_date=self.data['inflation']['inflation_data']['is_date'],
            next_meeting_date=self.data['inflation']['inflation_data']['is_date']
        )
        session.add(inflation_goal)
        await session.flush()

    async def save_key_rate(self, session: AsyncSession):
        key_rate = KeyRate(
            is_date=self.is_date,
            rate_value=self.data['key_rate_backup']['rate_value'],
            rate_change_date=self.data['key_rate_backup']['rate_change_date'],
            next_meeting_date=self.data['key_rate_backup']['next_meeting_date']
        )
        session.add(key_rate)
        await session.flush()

    async def save_interbank_rates(self, session: AsyncSession):
        for rate_name in self.data['interbank_rates'].keys():
            interbank_rate = InterbankRate(
                is_date=self.is_date,
                rate_name=rate_name,
                rate_today=self.data['interbank_rates'][rate_name]['rate_today'],
                rate_tomorrow=self.data['interbank_rates'][rate_name]['rate_tomorrow']
            )
            session.add(interbank_rate)
            await session.flush()

    async def save_currency_rates(self, session: AsyncSession):
        for rate_name in self.data['currency_rates'].keys():
            currency_rate = CurrencyRate(
                is_date=self.is_date,
                rate_name=rate_name,
                rate_today=self.data['currency_rates'][rate_name]['rate_today'],
                rate_tomorrow=self.data['currency_rates'][rate_name]['rate_tomorrow']
            )
            session.add(currency_rate)
            await session.flush()

    async def save_metal_prices(self, session: AsyncSession):
        for metal_name in self.data['metal_prices'].keys():
            metal_price = MetalPrice(
                is_date=self.is_date,
                metal_name=metal_name,
                price_today=self.data['metal_prices'][metal_name]['price_today'],
                price_tomorrow=self.data['metal_prices'][metal_name]['price_tomorrow']
            )
            session.add(metal_price)
            await session.flush()

    async def save_reserve(self, session: AsyncSession):
        reserve = Reserve(
            is_date=self.is_date,
            rate_date=self.data['reserves']['rate_date'],
            reserve_value=self.data['reserves']['reserve_value']
        )
        session.add(reserve)
        await session.flush()

    async def save_bank_requirements(self, session: AsyncSession):
        for requirement_name, rate_value in self.data['bank_requirements'].items():
            interbank_rate = BankRequirement(
                is_date=self.is_date,
                requirement_name=requirement_name,
                rate_value=rate_value
            )
            session.add(interbank_rate)
            await session.flush()


cbr_db_manager = CBR_DB_Manager()
asyncio.run(cbr_db_manager.run())
