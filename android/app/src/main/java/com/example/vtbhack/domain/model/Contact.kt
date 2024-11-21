package com.example.vtbhack.domain.model

data class Contact(
    val name: String,
    val phonenumber: String,
    var role: String = "просмотр"
)