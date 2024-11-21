package com.example.vtbhack.data

import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.GoalPost
import com.example.vtbhack.domain.model.InvitationAnswerPost
import com.example.vtbhack.domain.model.InvitationPost
import com.example.vtbhack.domain.model.InvitationResponsePost
import com.example.vtbhack.domain.model.SurveyPost


class MainRepository(private val apiHelper: ApiHelper) {

    suspend fun getCurrentUser(token: String) = apiHelper.getCurrentUser(token)

    suspend fun getAccumulatedAccounts(token: String) = apiHelper.getAccumulatedAccounts(token)

    suspend fun getRecommendedDeposit(token: String, date: String) = apiHelper.getRecommendedDeposit(token, date)

    suspend fun getGoalInfo(token: String, id: Int) = apiHelper.getGoalInfo(token, id)

    suspend fun postAccount(token: String, account: AccumulatedAccountPost) = apiHelper.postAccount(token, account)

    suspend fun postInvitationAnswer(token: String, answer: InvitationAnswerPost) = apiHelper.postInvitationAnswer(token, answer)

    suspend fun postGoal(token: String, goal: GoalPost) = apiHelper.postGoal(token, goal)

    suspend fun postSurvey(token: String, surveyPost: SurveyPost) = apiHelper.postSurvey(token, surveyPost)

    suspend fun getSurvey(token: String) = apiHelper.getSurvey(token)

    suspend fun invite(token: String, invitation: InvitationPost) = apiHelper.invite(token, invitation)

    suspend fun confirmInvitation(token: String, invitationResponse: InvitationResponsePost) = apiHelper.confirmInvitation(token, invitationResponse)

}