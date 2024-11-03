from bs4 import BeautifulSoup

from loguru import logger

from backend.cbr.cbr_fetch_manager import CBR_FetchManager


class CBR_ExtendParser(CBR_FetchManager):
    BASE_EXTEND_URL: str = "https://cbr.ru/key-indicators/"

    @staticmethod
    def parse_inflation(soup: BeautifulSoup) -> dict:
        inflation_section = soup.find('div', class_='key-indicators_intro')
        data: dict = {}
        if inflation_section:
            try:
                data['inflation_goals'] = inflation_section.select_one('.value').text.strip()
                data['inflation_data'] = {
                    'rate_value': inflation_section.select('.value')[1].text.strip(),
                    'is_date': inflation_section.select('.denotement')[1].text.strip()
                }
            except (IndexError, AttributeError):
                logger.info("Ошибка извлечения данных по инфляции")

        return data

    @staticmethod
    def parse_key_rate(soup: BeautifulSoup) -> dict:
        """
            Ключевая ставка
        """
        key_rate_section = soup.find('div', class_='main-indicator')
        if key_rate_section:
            try:
                return {
                    'rate_value': key_rate_section.find('div', class_='main-indicator_value').text.strip(),
                    'rate_change_date': key_rate_section.find('div', class_='main-indicator_text').text.strip()
                }
            except AttributeError:
                logger.info("Ошибка извлечения данных по ключевой ставке")
                return {
                    'rate_value': None,
                    'rate_change_date': None
                }

    @staticmethod
    def parse_interbank_rates(soup: BeautifulSoup) -> dict:
        """
            Ставки межбанковского кредитного рынка
        """
        interbank_rates = {}
        interbank_table = soup.find('div', class_='key-indicator_content offset-md-2')
        if interbank_table:
            rows = interbank_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    rate_name = " ".join(cells[0].text.split())
                    rate_today = cells[1].text.strip()
                    rate_tomorrow = cells[2].text.strip() if len(cells) > 2 else 'Нет данных'
                    interbank_rates[rate_name] = {'rate_today': rate_today, 'rate_tomorrow': rate_tomorrow}
        return interbank_rates

    @staticmethod
    def parse_currency_rates(soup: BeautifulSoup) -> dict:
        """
            Курсы валют
        """
        currency_data = {}
        currency_table = soup.find_all('div', class_='key-indicator_content offset-md-2')[1]
        if currency_table:
            currency_rows = currency_table.find_all('tr')
            for row in currency_rows[1:]:
                cells = row.find_all('td')
                if len(cells) > 2:
                    currency_name = " ".join(cells[0].text.split())
                    rate_today = cells[1].text.strip()
                    rate_tomorrow = cells[2].text.strip()
                    currency_data[currency_name] = {'rate_today': rate_today, 'rate_tomorrow': rate_tomorrow}
        return currency_data

    @staticmethod
    def parse_metal_prices(soup: BeautifulSoup) -> dict:
        """
            Учетные цены на драгоценные металлы
        """
        metals_data = {}
        metals_table = soup.find_all('div', class_='key-indicator_content offset-md-2')[2]
        if metals_table:
            metal_rows = metals_table.find_all('tr')
            for row in metal_rows[1:]:
                cells = row.find_all('td')
                if len(cells) > 2:
                    metal_name = " ".join(cells[0].text.split())
                    price_today = cells[1].text.strip()
                    price_tomorrow = cells[2].text.strip()
                    metals_data[metal_name] = {'price_today': price_today, 'price_tomorrow': price_tomorrow}
        return metals_data

    @staticmethod
    def parse_reserves(soup: BeautifulSoup) -> dict:
        """
            Международные резервы Российской Федерации
        """
        reserves_section = soup.find('div', text=lambda x: x and 'Международные резервы Российской Федерации' in x)
        if reserves_section:
            reserves_date = reserves_section.find_next('a').text.strip() if reserves_section.find_next('a') else 'Нет данных'
            reserves_value = reserves_section.find_next(
                'div', class_='value'
            ).text.strip() if reserves_section.find_next('div', class_='value') else 'Нет данных'
            return {'is_date': reserves_date, 'reserve_value': reserves_value}

    @staticmethod
    def parse_liquidity_indicators(soup: BeautifulSoup) -> dict:
        """
            Показатели ликвидности банковского сектора
        """
        liquidity_data = {}
        liquidity_section = soup.find_all('div', class_='key-indicator_content offset-md-2')[3]
        if liquidity_section:
            liquidity_rows = liquidity_section.find_all('tr')
            for row in liquidity_rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    indicator_name = " ".join(cells[0].text.split())
                    indicator_value = cells[1].text.strip()
                    liquidity_data[indicator_name] = indicator_value
        return liquidity_data

    @staticmethod
    def parse_bank_requirements(soup: BeautifulSoup) -> dict:
        """
            Требования Банка России к кредитным организациям
        """
        data = {}
        requirements_section = soup.find_all('div', class_='key-indicator_content offset-md-2')[4]
        if requirements_section:
            requirements_rows = requirements_section.find_all('tr')
            for row in requirements_rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    requirement_name = " ".join(cells[0].text.split())
                    requirement_value = cells[1].text.strip()
                    data[requirement_name] = requirement_value
        return data
