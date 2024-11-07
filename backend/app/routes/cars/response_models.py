cars_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            'id': 1,
                            "model_car": "Toyota Camry",
                            "year": 2005,
                            "transmission_type": "Automatic",
                            "body_type": "Sedan",
                            "fuel_type": "Petrol",
                            "average_price": 1700000,
                            "status": "Used"
                        }
                    },
                }
            }
        }
    }
}
