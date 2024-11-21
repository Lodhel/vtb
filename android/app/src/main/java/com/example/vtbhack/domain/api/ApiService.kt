package com.example.vtbhack.domain.api

import com.example.vtbhack.domain.model.AccumulatedAccountData
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.GoalData
import com.example.vtbhack.domain.model.GoalPost
import com.example.vtbhack.domain.model.InvitationAnswerPost
import com.example.vtbhack.domain.model.InvitationPost
import com.example.vtbhack.domain.model.InvitationResponsePost
import com.example.vtbhack.domain.model.RecommendedDeposit
import com.example.vtbhack.domain.model.RecommendedDepositData
import com.example.vtbhack.domain.model.SingleAccumulatedAccountData
import com.example.vtbhack.domain.model.StatusResponse
import com.example.vtbhack.domain.model.SurveyPost
import com.example.vtbhack.domain.model.SurveyResponse
import com.example.vtbhack.domain.model.SurveyResponseData
import com.example.vtbhack.domain.model.User
import com.example.vtbhack.domain.model.UserData
import com.example.vtbhack.domain.model.UserProfileData
import retrofit2.http.*


interface ApiService {

    @GET("auth")
    suspend fun getCurrentUser(@Header("Authorization") token: String): UserData

    @GET("accumulated_accounts")
    suspend fun getAccumulatedAccounts(@Header("Authorization") token: String): AccumulatedAccountData

    @GET("recommended-deposits")
    suspend fun getRecommendedDeposit(@Header("Authorization") token: String, @Query("rate_date") date: String): RecommendedDepositData

    //@GET("card")
    //suspend fun getCards(@Header("Authorization") token: String): AccumulatedAccountData

    @GET("goal")
    suspend fun getGoalInfo(@Header("Authorization") token: String, @Query("account_id") id: Int): GoalData

    @POST("accumulated_accounts")
    suspend fun postAccount(@Header("Authorization") token: String, @Body account: AccumulatedAccountPost): SingleAccumulatedAccountData

    @POST("accumulated_accounts/invite/confirm")
    suspend fun postInvitationAnswer(@Header("Authorization") token: String, @Body answer: InvitationAnswerPost): SingleAccumulatedAccountData

    @POST("user_profile")
    suspend fun postSurvey(@Header("Authorization") token: String, @Body surveyPost: SurveyPost): SurveyResponseData

    @GET("user_profile")
    suspend fun getSurvey(@Header("Authorization") token: String): UserProfileData

    @POST("accumulated_accounts/invite")
    suspend fun invite(@Header("Authorization") token: String, @Body invitation: InvitationPost): StatusResponse

    @POST("accumulated_accounts/invite/confirm")
    suspend fun confirmInvitation(@Header("Authorization") token: String, @Body invitationResponse: InvitationResponsePost): AccumulatedAccountData

    @POST("goal")
    suspend fun postGoal(@Header("Authorization") token: String, @Body goal: GoalPost): GoalData

}