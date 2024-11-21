package com.example.vtbhack.domain.model

data class GoalPost(
    val account_id:Int,
    val description: String,
    val target_amount: Double,
    val months_remaining: Int,
)
