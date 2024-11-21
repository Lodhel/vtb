package com.example.vtbhack.domain.model

data class InvitationPost(
    val account_id: Int,
    val invited_user_phone: String,
    val role: String = "просмотр"
)
