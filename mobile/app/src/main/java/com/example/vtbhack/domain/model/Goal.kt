package com.example.vtbhack.domain.model

data class Goal(
    var description: String,
    var target_amount: Double,
    var recommended_contribution: Double,
    var progress_percentage: Double,
    var rate_date: String
)
