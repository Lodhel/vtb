package com.example.vtbhack.data

import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.GoalPost


class MainRepository(private val apiHelper: ApiHelper) {

    suspend fun getAccumulatedAccounts(token: String) = apiHelper.getAccumulatedAccounts(token)

    suspend fun getGoalInfo(token: String, id: Int) = apiHelper.getGoalInfo(token, id)

    suspend fun postAccount(token: String, account: AccumulatedAccountPost) = apiHelper.postAccount(token, account)

    suspend fun postGoal(token: String, goal: GoalPost) = apiHelper.postGoal(token, goal)
}