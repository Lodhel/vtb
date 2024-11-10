package com.example.vtbhack.domain.model

data class User(
    val id: Int,
    val name: String,
    var lastname: String,
    var phone_number: String,
    var email: String,
    var vtb_auth: String,
    var token_auth: String,
)