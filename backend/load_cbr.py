import asyncio

from backend.cbr.cbr_extend_parser import CBR_ExtendParser
from backend.cbr.cbr_parser import CBRParser


class CBR_Loader(CBRParser, CBR_ExtendParser):

    def __init__(self):
        super(CBR_Loader, self).__init__()
        self.data: dict = {}

    async def run(self):
        await self.parse_extend_page()
        await self.parse_main_page()

        return self.data

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


cbr_loader = CBR_Loader()
asyncio.run(cbr_loader.run())
