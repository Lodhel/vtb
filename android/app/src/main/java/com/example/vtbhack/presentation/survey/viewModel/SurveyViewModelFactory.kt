package com.example.vtbhack.presentation.survey.viewModel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.data.MainRepository
import com.example.vtbhack.domain.api.ApiHelper

class SurveyViewModelFactory(private val apiHelper: ApiHelper) :
    ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(SurveyViewModel::class.java)) {
            return SurveyViewModel(MainRepository(apiHelper)) as T
        }
        throw IllegalArgumentException("Unknown class name")
    }
}