from datetime import datetime

from bs4 import BeautifulSoup

from backend.cbr.cbr_fetch_manager import CBR_FetchManager


class CBRParser(CBR_FetchManager):
    BASE_URL: str = "https://cbr.ru/"

    @staticmethod
    def parse_inflation_backup(soup: BeautifulSoup) -> str:
        """
            Цель по инфляции
        """
        inflation_block = soup.find_all('div', class_='main-indicator')[0]
        if inflation_block:
            return inflation_block.find('div', class_='main-indicator_value').text.strip()

    @staticmethod
    def parse_key_rate_backup(soup: BeautifulSoup) -> dict:
        """
            Ключевая ставка
        """
        key_rate_block = soup.find_all('div', class_='main-indicator')[2]
        rate_value: str = key_rate_block.find('div', class_='main-indicator_value').text.strip()
        rate_change_date: str = key_rate_block.find('div', class_='main-indicator_text').text.strip().replace('с ', '')
        next_meeting_date: str = key_rate_block.find('div', class_='main-indicator_comment-date').text.strip()

        if key_rate_block:
            return {
                'rate_value': float(rate_value.replace(',', '.').replace(' ', '').replace('%', '')),
                'rate_change_date': datetime.strptime(rate_change_date, '%d.%m.%Y').date(),
                'next_meeting_date': datetime.strptime(next_meeting_date, '%d.%m.%Y').date()
            }

    @staticmethod
    def parse_ruonia_rate(soup: BeautifulSoup) -> dict:
        """
            Ставка RUONIA
        """
        ruonia_block = soup.find_all('div', class_='main-indicator')[3]
        if ruonia_block:
            return {
                'rate_value': ruonia_block.find('div', class_='main-indicator_value').text.strip(),
                'is_date': ruonia_block.find('div', class_='main-indicator_text').text.strip()
            }

    @staticmethod
    def parse_currency_rates_backup(soup: BeautifulSoup) -> dict:
        rates_table = soup.find('div', class_='main-indicator_rates-table')
        if rates_table:
            currencies = rates_table.find_all('div', class_='main-indicator_rate')
            exchange_rates = {}
            for currency in currencies:
                name_elem = currency.find('div', class_='col-md-2 col-xs-9')
                rate_today_elem = currency.find_all('div', class_='mono-num')
                if name_elem and rate_today_elem and len(rate_today_elem) > 1:
                    name = name_elem.text.strip().replace(',', '')
                    rate_today = rate_today_elem[0].text.strip()
                    rate_tomorrow = rate_today_elem[1].text.strip()
                    exchange_rates[name] = {'rate_today': rate_today, 'rate_tomorrow': rate_tomorrow}

            return exchange_rates
