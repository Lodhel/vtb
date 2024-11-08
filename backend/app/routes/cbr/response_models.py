cbr_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            "inflation_goal": [
                                {
                                    "id": 9,
                                    "rate_value": 4.0,
                                    "is_date": "2024-11-08"
                                }
                            ],
                            "inflation_data": [
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 8.6,
                                    "id": 7,
                                    "period": "Сентябрь 2024"
                                }
                            ],
                            "key_rate": [
                                {
                                    "id": 7,
                                    "rate_change_date": "2024-10-28",
                                    "rate_value": 21.0,
                                    "next_meeting_date": "2024-12-20",
                                    "is_date": "2024-11-08"
                                }
                            ],
                            "interbank_rate": [
                                {
                                    "rate_tomorrow": "2-7 дней",
                                    "id": 25,
                                    "rate_name": "% годовых",
                                    "rate_today": "1 день",
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "rate_tomorrow": "",
                                    "id": 26,
                                    "rate_name": "RUONIA за 07.11.2024",
                                    "rate_today": "20,30",
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "rate_tomorrow": "18,99",
                                    "id": 27,
                                    "rate_name": "Срочная версия RUONIA 08.11.2024",
                                    "rate_today": "19,44",
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "rate_tomorrow": "—",
                                    "id": 28,
                                    "rate_name": "MIACR за 07.11.2024",
                                    "rate_today": "20,35",
                                    "is_date": "2024-11-08"
                                }
                            ],
                            "currency_rate": [
                                {
                                    "is_date": "2024-11-08",
                                    "rate_today": 13.6395,
                                    "rate_tomorrow": 13.624,
                                    "id": 16,
                                    "currency_name": "Китайский юань 1 CNY"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_today": 98.2236,
                                    "rate_tomorrow": 98.0726,
                                    "id": 17,
                                    "currency_name": "Доллар США 1 USD"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_today": 105.7086,
                                    "rate_tomorrow": 105.5679,
                                    "id": 18,
                                    "currency_name": "Евро 1 EUR"
                                }
                            ],
                            "metal_price": [
                                {
                                    "id": 21,
                                    "price_tomorrow": 8387.89,
                                    "metal_name": "Золото Au",
                                    "price_today": 8660.86,
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "id": 22,
                                    "price_tomorrow": 100.27,
                                    "metal_name": "Серебро Ag",
                                    "price_today": 103.11,
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "id": 23,
                                    "price_tomorrow": 3067.97,
                                    "metal_name": "Платина Pt",
                                    "price_today": 3161.12,
                                    "is_date": "2024-11-08"
                                },
                                {
                                    "id": 24,
                                    "price_tomorrow": 3272.92,
                                    "metal_name": "Палладий Pd",
                                    "price_today": 3448.49,
                                    "is_date": "2024-11-08"
                                }
                            ],
                            "reserve": [
                                {
                                    "rate_date": "2024-11-01",
                                    "id": 5,
                                    "is_date": "2024-11-08",
                                    "reserve_value": None
                                }
                            ],
                            "liquidity_indicator": [],
                            "bank_requirement": [
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": None,
                                    "id": 37,
                                    "requirement_name": "млрд руб."
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": -124.6,
                                    "id": 38,
                                    "requirement_name": "Дефицит/профицит ликвидности банковского сектора на 08.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": None,
                                    "id": 39,
                                    "requirement_name": "Сведения об остатках средств на корреспондентских счетах кредитных организаций"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 2542.9,
                                    "id": 40,
                                    "requirement_name": "по Российской Федерации на 08.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 2305.6,
                                    "id": 41,
                                    "requirement_name": "по Московскому региону на 08.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 1921.9,
                                    "id": 42,
                                    "requirement_name": "Объем предоставленных внутридневных кредитов на 07.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 7201.0,
                                    "id": 43,
                                    "requirement_name": "Депозиты банков в Банке России на 08.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 0.0,
                                    "id": 44,
                                    "requirement_name": "ОБР в обращении на 08.11.2024"
                                },
                                {
                                    "is_date": "2024-11-08",
                                    "rate_value": 1163.9,
                                    "id": 45,
                                    "requirement_name": "Сальдо операций Банка России по предоставлению/абсорбированию ликвидности на 08.11.2024"
                                }
                            ]
                        }
                    },
                }
            }
        }
    }
}
