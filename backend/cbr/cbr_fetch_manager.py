import httpx
from bs4 import BeautifulSoup
from typing import Optional


class CBR_FetchManager:
    @staticmethod
    async def fetch_content(url: str) -> Optional[BeautifulSoup]:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            print(f"Ошибка при запросе к {url}: {response.status_code}")
            return None
