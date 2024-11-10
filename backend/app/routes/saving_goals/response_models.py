user_goal_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            "description": "Накопить на отпуск",
                            "target_amount": 100000.0,
                            "recommended_contribution": 5000.0,
                            "progress_percentage": 30.0
                        }
                    }
                }
            }
        }
    }
}
