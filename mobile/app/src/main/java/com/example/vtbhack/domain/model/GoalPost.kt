package com.example.vtbhack.domain.model

data class GoalPost(
    var account_id:Int,
    var description: String,
    var target_amount: Double,
    var months_remaining: Int,
)
