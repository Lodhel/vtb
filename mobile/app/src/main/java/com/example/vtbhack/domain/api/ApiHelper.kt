package com.example.vtbhack.domain.api

import com.example.vtbhack.domain.model.AccumulatedAccountData
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.domain.model.GoalData
import com.example.vtbhack.domain.model.GoalPost
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

class ApiHelper(private val apiService: ApiService) {

    suspend fun getAccumulatedAccounts(token: String) = apiService.getAccumulatedAccounts(token)

    suspend fun getGoalInfo(token: String, id: Int) = apiService.getGoalInfo(token, id)

    suspend fun postAccount(token: String, account: AccumulatedAccountPost) = apiService.postAccount(token, account)

    suspend fun postGoal(token: String, goal: GoalPost) = apiService.postGoal(token, goal)

}