package com.example.vtbhack.domain.model

data class UserProfile(
    val id: Int,
    val income_last_month: Int,
    val expenses_last_month: Int,
    val savings_last_month: Int,
    val marital_status: Boolean,
    val children_count: Int,
    val education: String,
    val occupation: String,
)