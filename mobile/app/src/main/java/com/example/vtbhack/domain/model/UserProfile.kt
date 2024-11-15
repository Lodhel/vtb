package com.example.vtbhack.domain.model

data class UserProfile(
    val id: Int,
    val income_last_month: Int,
    var expenses_last_month: Int,
    var savings_last_month: Int,
    var marital_status: Boolean,
    var children_count: Int,
    var education: String,
    var occupation: String,
)