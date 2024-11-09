import httpx

from backend.app.vtb_services.vtb_client import VTB_AUTH_CLIENT


class VTB_AccountsManager(VTB_AUTH_CLIENT):

    async def get_accounts_data(self) -> dict:
        accounts = await self.get_accounts()
        return {
            account['accountId']: await self.get_account(account['accountId'])
            for account in accounts
        }

    async def get_accounts(self) -> list:
        """
            :return: [
                {
                    'accountId': '348f3e87-aad3-4197-8bc6-9a23da255c67',
                    'status': 'Enabled',
                    'currency': 'RUB',
                    'accountType': 'Personal',
                    'accountSubType': 'CurrentAccount',
                    'schemeName': 'RU.CBR.AccountNumber',
                    'identification': '45952763460701835055',
                    'name': 'Основной текущий счет'
                }
            ]
        """
        async with httpx.AsyncClient(verify=False) as client:
            headers = await self.get_headers(client)
            response = await client.get(f'{self.BASE_VTB_API_URL}accounts', headers=headers)
            data: dict = response.json()
            try:
                return data['Data']['Account']
            except KeyError:
                return []

    async def get_account(self, account_id: str) -> dict:
        async with httpx.AsyncClient(verify=False) as client:
            headers = await self.get_headers(client)
            response = await client.get(f'{self.BASE_VTB_API_URL}accounts/{account_id}', headers=headers)
            return response.json()

    async def get_balance(self, account_id: str) -> dict:
        async with httpx.AsyncClient(verify=False) as client:
            headers = await self.get_headers(client)
            response = await client.get(f'{self.BASE_VTB_API_URL}accounts/{account_id}/balance', headers=headers)
            data: dict = response.json()
            try:
                return data['Data']
            except KeyError:
                return {}
