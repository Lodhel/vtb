package com.example.vtbhack.domain.model

data class User(
    val id: Int,
    var name: String,
    var lastname: String,
    var phone_number: String,
    var email: String,
    val vtb_auth: String,
    val token_auth: String,
)