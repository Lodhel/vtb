package com.example.vtbhack.domain.model

data class AccumulatedAccount(
    val id: Int,
    val owner_id: Int,
    val amount: Int,
    val currency: String,
    val account_type: String,
    val created_at: String,
    val users: Users
)
