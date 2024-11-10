user_profile_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            'user_id': 1,
                            "income_last_month": 150000.0,
                            "expenses_last_month": 80000.0,
                            "savings_last_month": 20000.0,
                            "marital_status": True,
                            "children_count": 2,
                            "education": "высшее",
                            "occupation": "работник частной компании"
                        }
                    },
                }
            }
        }
    }
}
