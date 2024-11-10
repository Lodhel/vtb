package com.example.vtbhack.domain.model

data class AccumulatedAccount(
    val id: Int,
    val owner_id: Int,
    var amount: Int,
    var currency: String,
    var created_at: String,
)
