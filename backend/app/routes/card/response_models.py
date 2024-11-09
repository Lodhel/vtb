card_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            'accountId': 'a502db73-0c2c-483b-b7b7-cb8393221698',
                            'balance': {
                                'amount': {
                                    'currency': 'RUB',
                                    'amount': '913.24'
                                },
                                'creditDebitIndicator': 'Credit',
                                'type': 'ClosingAvailable'
                            }
                        }
                    },
                }
            }
        }
    }
}
