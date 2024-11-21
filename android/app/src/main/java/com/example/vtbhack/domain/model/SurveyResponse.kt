package com.example.vtbhack.domain.model

data class SurveyResponse(
    val user_id: Int,
    val income_last_month: Double,
    val expenses_last_month: Double,
    val savings_last_month: Double,
    val marital_status: Boolean,
    val children_count: Int,
    val education: String,
    val occupation: String,
)
