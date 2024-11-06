cars_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            "Model": "Toyota Camry",
                            "Year": 2005,
                            "TransmissionType": "Automatic",
                            "BodyType": "Sedan",
                            "FuelType": "Petrol",
                            "AveragePrice": 1700000,
                            "Status": "Used"
                        }
                    },
                }
            }
        }
    }
}
