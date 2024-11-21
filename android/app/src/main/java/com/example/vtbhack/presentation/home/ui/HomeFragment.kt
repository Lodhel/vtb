package com.example.vtbhack.presentation.home.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentHomeBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.AccumulatedAccount
import com.example.vtbhack.domain.model.Goal
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory
import com.example.vtbhack.presentation.survey.ui.FormIncomeFragment

class HomeFragment : Fragment(R.layout.fragment_home) {
    private lateinit var binding: FragmentHomeBinding
    private lateinit var homeViewModel: HomeViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        homeViewModel = ViewModelProvider(
            requireActivity(), HomeViewModelFactory(
                ApiHelper(
                    RetrofitBuilder.apiService
                )
            )
        )[HomeViewModel::class.java]
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentHomeBinding.bind(view)

        initialiseObservers()
        initialiseUIElements()
    }

    @SuppressLint("SimpleDateFormat", "DefaultLocale", "SetTextI18n")
    private fun initialiseObservers() {
        homeViewModel.getRecommendedDeposit(MainActivity.authToken)
        homeViewModel.recommendedDeposit.observe(viewLifecycleOwner) {
            if (it.recommended_deposit == 0.0) {
                binding.depositInfo.visibility = View.GONE
                binding.surveyInfo.visibility = View.VISIBLE
                binding.doSurveyBtn.setOnClickListener {
                    setCurrentFragment(FormIncomeFragment())
                }
            }
            else {
                binding.depositInfo.visibility = View.VISIBLE
                binding.surveyInfo.visibility = View.GONE
                binding.recommendedAmount.text = "${String.format("%.2f", it.recommended_deposit)} руб."
            }
        }

        homeViewModel.getCurrentUser(MainActivity.authToken)
        homeViewModel.getGoals(MainActivity.authToken)
        /*homeViewModel.currentUser.observe(viewLifecycleOwner) {
            homeViewModel.getGoals(authToken)
            //homeViewModel.getInvitations(authToken)
        }*/

        homeViewModel.goals.observe(viewLifecycleOwner) {
            setUpGoalsRV(it)
        }
        homeViewModel.accounts.observe(viewLifecycleOwner) {
            setUpAccountsRV(it)
        }
    }

    private fun initialiseUIElements() {
        binding.goalsAddFirstBtn.setOnClickListener {
            setCurrentFragment(AddAccountTypeFragment.newInstance("goal"), null)
        }
        binding.goalsAddBtn.setOnClickListener {
            setCurrentFragment(AddAccountTypeFragment.newInstance("goal"), null)
        }
        binding.addProduct.setOnClickListener {
            setCurrentFragment(AddProductTypeFragment.newInstance(), null)
        }

    }

    private fun setUpGoalsRV(goalsList: List<Goal>) {
        val goalsAdapter = GoalsAdapter(goalsList, ::onGoalClicked)
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
        binding.goalsRV.layoutManager = linearLayoutManager
        binding.goalsRV.adapter = goalsAdapter
        checkEmptyState(goalsList)
    }

    private fun setUpAccountsRV(accountsList: List<AccumulatedAccount>) {
        val goalsAdapter = AccountsAdapter(accountsList, ::onAccountClicked)
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.VERTICAL, false)
        binding.accountsRV.layoutManager = linearLayoutManager
        binding.accountsRV.adapter = goalsAdapter
    }

    private fun onAccountClicked(account_id: Int) {
        setCurrentFragment(AccountInfoFragment.newInstance(account_id))
    }

    private fun onGoalClicked(account_id: Int) {
        setCurrentFragment(GoalInfoFragment.newInstance(account_id))
    }

    private fun checkEmptyState(list: List<Goal>): Boolean {
        if (list.isEmpty()) {
            binding.goalsAddFirstBtn.visibility = View.VISIBLE
            binding.goalsAddBtn.visibility = View.GONE
            return true
        }
        binding.goalsAddFirstBtn.visibility = View.GONE
        binding.goalsAddBtn.visibility = View.VISIBLE
        return false
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            addToBackStack(name)
            commit()
        }

    companion object {
        @JvmStatic
        fun newInstance() = HomeFragment()
    }
}