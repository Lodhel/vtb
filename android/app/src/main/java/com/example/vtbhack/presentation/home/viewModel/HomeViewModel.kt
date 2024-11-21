package com.example.vtbhack.presentation.home.viewModel

import android.annotation.SuppressLint
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.vtbhack.data.MainRepository
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.model.AccumulatedAccount
import com.example.vtbhack.domain.model.AccumulatedAccountPost
import com.example.vtbhack.domain.model.Contact
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.domain.model.GoalPost
import com.example.vtbhack.domain.model.InvitationPost
import com.example.vtbhack.domain.model.InvitedUser
import com.example.vtbhack.domain.model.Owner
import com.example.vtbhack.domain.model.RecommendedDeposit
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar

class HomeViewModel(private val mainRepository: MainRepository) : ViewModel() {

    private val _currentUser = MutableLiveData<Owner>()
    val currentUser: LiveData<Owner> = _currentUser

    var selectedContacts: ArrayList<Contact> = ArrayList()

    private val _accounts = MutableLiveData<List<AccumulatedAccount>>()
    val accounts: LiveData<List<AccumulatedAccount>> = _accounts

    private val _invitations = MutableLiveData<List<AccumulatedAccount>>()
    val invitations: LiveData<List<AccumulatedAccount>> = _invitations

    private val _goals = MutableLiveData<List<Goal>>()
    val goals: LiveData<List<Goal>> = _goals

    private val _surveyDone = MutableLiveData<Boolean>()
    val surveyDone: LiveData<Boolean> = _surveyDone

    val loadingStateLiveData = MutableLiveData<LoadingState>()
    val accountLoadingStateLiveData = MutableLiveData<LoadingState>()

    private val _recommendedDeposit = MutableLiveData<RecommendedDeposit>()
    val recommendedDeposit: LiveData<RecommendedDeposit> = _recommendedDeposit

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

    fun getSurvey(token: String) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val survey = mainRepository.getSurvey(token)
                _surveyDone.postValue(true)
            } catch (e: Exception) {
                _surveyDone.postValue(false)
            }
        }
    }

    fun getCurrentUser(token: String) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val user = mainRepository.getCurrentUser(token).data
                _currentUser.postValue(Owner(user.name, user.lastname))
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }

    fun getAccumulatedAccounts(token: String) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val accounts = mainRepository.getAccumulatedAccounts(token).data
                _accounts.postValue(accounts)
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }

    fun getInvitations(token: String) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val inv = mainRepository.getAccumulatedAccounts(token).data.filter {
                    it.users.invited_users.contains(
                        InvitedUser(
                            currentUser.value!!.name,
                            currentUser.value!!.lastname,
                            "просмотр",
                            "ожидает подтверждения"
                        )
                    ) || it.users.invited_users.contains(
                        InvitedUser(
                            currentUser.value!!.name,
                            currentUser.value!!.lastname,
                            "вкладчик",
                            "ожидает подтверждения"
                        )
                    ) || it.users.invited_users.contains(
                        InvitedUser(
                            currentUser.value!!.name,
                            currentUser.value!!.lastname,
                            "полный доступ",
                            "ожидает подтверждения"
                        )
                    )
                }
                _invitations.postValue(inv)
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }

    fun getGoals(token: String) {
        accountLoadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val accounts = mainRepository.getAccumulatedAccounts(token).data.distinct()
                _accounts.postValue(accounts)
                val goalsList = ArrayList<Goal>()
                for (account in accounts) {
                    try {
                        val goalInfo = mainRepository.getGoalInfo(token, account.id).data
                        goalsList.add(
                            goalInfo.copy(
                                account_id = account.id,
                                progress_percentage = account.amount / goalInfo.target_amount * 100,
                                joint = account.users.invited_users.isNotEmpty()
                            )
                        )
                    } catch (e: Exception) {}
                }
                _goals.postValue(goalsList)
                accountLoadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                accountLoadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }

    fun inviteSelectedContacts(token: String, account_id: Int) {
        selectedContacts.forEach {
            loadingStateLiveData.value = LoadingState.LOADING
            viewModelScope.launch(Dispatchers.IO) {
                try {
                    mainRepository.invite(
                        token,
                        InvitationPost(account_id, it.phonenumber, it.role)
                    )
                    loadingStateLiveData.postValue(LoadingState.SUCCESS)
                } catch (e: Exception) {
                    loadingStateLiveData.postValue(LoadingState.ERROR)
                }
            }
        }
        clearSelectedContacts()
    }

    fun clearSelectedContacts() {
        selectedContacts = ArrayList()
    }

    fun addNewAccount(
        token: String,
        amount: Double = 0.0,
        currency: String = "RUB",
        type: String = "Личный",
        invitations: Boolean = false
    ) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val new_account = mainRepository.postAccount(
                    token,
                    AccumulatedAccountPost(amount, currency, type)
                )
                if (invitations) {
                    inviteSelectedContacts(token, new_account.data.id)
                }
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
        type: String = "Личный",
        description: String,
        target_amount: Double,
        months_remaining: Int,
        invitations: Boolean = false
    ) {
        loadingStateLiveData.value = LoadingState.LOADING
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val new_account = mainRepository.postAccount(
                    token,
                    AccumulatedAccountPost(amount, currency, type)
                )
                val account_id = new_account.data.id
                val new_goal = mainRepository.postGoal(
                    token,
                    GoalPost(account_id, description, target_amount, months_remaining)
                )
                if (invitations) {
                    inviteSelectedContacts(token, new_account.data.id)
                }
                loadingStateLiveData.postValue(LoadingState.SUCCESS)
            } catch (e: Exception) {
                loadingStateLiveData.postValue(LoadingState.ERROR)
            }
        }
    }
}