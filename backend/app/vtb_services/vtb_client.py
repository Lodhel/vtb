import httpx

from backend.app.config import CLIENT_SECRET


class VTB_AUTH_CLIENT:

    BASE_VTB_API_URL: str = 'https://api.bankingapi.ru/extapi/aft/clientInfo/hackathon/v1/'

    @classmethod
    async def get_headers(cls, client: httpx.AsyncClient | None = None) -> dict:
        access_token: str = await cls.get_access_token(client)
        return {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    async def get_access_token(client: httpx.AsyncClient | None) -> str:
        base_url: str = 'https://auth.bankingapi.ru/auth/realms/kubernetes/protocol/openid-connect/token'

        data: dict = {
            "grant_type": "client_credentials",
            "client_id": "team020",
            "client_secret": CLIENT_SECRET
        }

        if client:
            response = await client.post(base_url, data=data)
            return response.json().get('access_token')
        else:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(base_url, data=data)
                return response.json().get('access_token')

