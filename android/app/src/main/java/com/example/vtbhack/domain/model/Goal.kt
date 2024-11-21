package com.example.vtbhack.domain.model

data class Goal(
    var account_id: Int?,
    val description: String,
    val target_amount: Double = 0.0,
    val recommended_contribution: Double = 0.0,
    val progress_percentage: Double = 0.0,
    val rate_date: String,
    var joint: Boolean = false
)
