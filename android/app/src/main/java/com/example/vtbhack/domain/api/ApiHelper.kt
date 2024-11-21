package com.example.vtbhack.domain.api

import com.example.vtbhack.domain.model.AccumulatedAccountData
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.domain.model.GoalData
import com.example.vtbhack.domain.model.GoalPost
import com.example.vtbhack.domain.model.InvitationAnswerPost
import com.example.vtbhack.domain.model.InvitationPost
import com.example.vtbhack.domain.model.InvitationResponsePost
import com.example.vtbhack.domain.model.RecommendedDeposit
import com.example.vtbhack.domain.model.SingleAccumulatedAccountData
import com.example.vtbhack.domain.model.StatusResponse
import com.example.vtbhack.domain.model.SurveyPost
import com.example.vtbhack.domain.model.SurveyResponse
import com.example.vtbhack.domain.model.User
import com.example.vtbhack.domain.model.UserProfileData
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

class ApiHelper(private val apiService: ApiService) {

    suspend fun getCurrentUser(token: String) = apiService.getCurrentUser(token)

    suspend fun getAccumulatedAccounts(token: String) = apiService.getAccumulatedAccounts(token)

    suspend fun getRecommendedDeposit(token: String, date: String) = apiService.getRecommendedDeposit(token, date)

    suspend fun getGoalInfo(token: String, id: Int) = apiService.getGoalInfo(token, id)

    suspend fun postAccount(token: String, account: AccumulatedAccountPost) = apiService.postAccount(token, account)

    suspend fun postInvitationAnswer(token: String, answer: InvitationAnswerPost) = apiService.postInvitationAnswer(token, answer)


    suspend fun postGoal(token: String, goal: GoalPost) = apiService.postGoal(token, goal)

    suspend fun postSurvey(token: String, surveyPost: SurveyPost) = apiService.postSurvey(token, surveyPost)

    suspend fun getSurvey(token: String) = apiService.getSurvey(token)

    suspend fun invite(token: String, invitation: InvitationPost) = apiService.invite(token, invitation)

    suspend fun confirmInvitation(token: String, invitationResponse: InvitationResponsePost) = apiService.confirmInvitation(token, invitationResponse)

}