package com.example.vtbhack.domain.model

data class SurveyPost(
    var income_last_month: Double = 0.0,
    var expenses_last_month: Double = 0.0,
    var savings_last_month: Double = 0.0,
    var marital_status: Boolean = false,
    var children_count: Int = 0,
    var education: String = "среднее",
    var occupation: String = "работник частной компании",
)
