package com.example.vtbhack.domain.model

data class Users(
    val owner: Owner,
    val invited_users: List<InvitedUser>
)