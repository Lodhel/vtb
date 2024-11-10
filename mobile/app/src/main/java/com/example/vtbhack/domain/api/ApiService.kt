package com.example.vtbhack.domain.api

import com.example.vtbhack.domain.model.AccumulatedAccountData
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.domain.model.GoalData
import com.example.vtbhack.domain.model.GoalPost
import com.example.vtbhack.domain.model.SingleAccumulatedAccountData
import retrofit2.http.*


interface ApiService {

    @GET("accumulated_accounts")
    suspend fun getAccumulatedAccounts(@Header("Authorization") token: String): AccumulatedAccountData

    @GET("goal")
    suspend fun getGoalInfo(@Header("Authorization") token: String, @Query("account_id") id: Int): GoalData

    @POST("accumulated_accounts")
    suspend fun postAccount(@Header("Authorization") token: String, @Body account: AccumulatedAccountPost): SingleAccumulatedAccountData

    @POST("goal")
    suspend fun postGoal(@Header("Authorization") token: String, @Body goal: GoalPost): GoalData

}