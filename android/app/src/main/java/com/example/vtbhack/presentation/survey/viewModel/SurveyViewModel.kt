package com.example.vtbhack.presentation.survey.viewModel

import android.annotation.SuppressLint
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.vtbhack.data.MainRepository
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.model.RecommendedDeposit
import com.example.vtbhack.domain.model.SurveyPost
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar

class SurveyViewModel(private val mainRepository: MainRepository) : ViewModel() {

    var survey: SurveyPost = SurveyPost()

    private val _recommendedDeposit = MutableLiveData<RecommendedDeposit>()
    val recommendedDeposit: LiveData<RecommendedDeposit> = _recommendedDeposit

    val loadingStateLiveData = MutableLiveData<LoadingState>()

    @SuppressLint("SimpleDateFormat")
    fun getRecommendedDeposit(token: String) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val sdf = SimpleDateFormat("yyyy-MM")
                val currentDate = sdf.format(Calendar.getInstance().time)
                val deposit = mainRepository.getRecommendedDeposit(token, currentDate).data
                _recommendedDeposit.postValue(deposit)
            } catch (e: Exception) {
            }
        }
    }

    @SuppressLint("SimpleDateFormat")
    fun postSurvey(token: String) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val response = mainRepository.postSurvey(token, survey).data
                response.user_id
                val sdf = SimpleDateFormat("yyyy-MM")
                val currentDate = sdf.format(Calendar.getInstance().time)
                val deposit = mainRepository.getRecommendedDeposit(token, currentDate).data
                _recommendedDeposit.postValue(deposit)
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }
}