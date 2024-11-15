package com.example.vtbhack.presentation.home.viewModel

import androidx.lifecycle.*
import com.example.vtbhack.data.MainRepository
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.domain.model.GoalPost
import kotlinx.coroutines.*

class HomeViewModel(private val mainRepository: MainRepository) : ViewModel() {

    private val _goals = MutableLiveData<List<Goal>>()
    val goals: LiveData<List<Goal>> = _goals
    val loadingStateLiveData = MutableLiveData<LoadingState>()

    fun getGoals(token: String) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val goalsList = ArrayList<Goal>()
                val accounts = mainRepository.getAccumulatedAccounts(token)
                for (account in accounts.data) {
                    val goalInfo = mainRepository.getGoalInfo(token, account.id)
                    goalsList.add(goalInfo.data)
                }
                _goals.postValue(goalsList)
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }

    fun addNewGoal(
        token: String,
        amount: Double = 0.0,
        currency: String = "RUB",
        description: String,
        target_amount: Double,
        months_remaining: Int
    ) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val new_account = mainRepository.postAccount(token, AccumulatedAccountPost(amount, currency))
                val account_id = new_account.data.id
                val new_goal = mainRepository.postGoal(token, GoalPost(account_id, description, target_amount, months_remaining))
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }
}