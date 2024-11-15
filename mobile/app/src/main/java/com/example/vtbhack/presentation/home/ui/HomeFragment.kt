package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentHomeBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.Goal

class HomeFragment : Fragment(R.layout.fragment_home) {
    private lateinit var binding: FragmentHomeBinding
    private lateinit var homeViewModel: HomeViewModel

    //private lateinit var userId: String
    private val authToken: String = "VTBAuthToken9"

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

    private fun initialiseObservers() {
        homeViewModel.getGoals(authToken)

        homeViewModel.goals.observe(viewLifecycleOwner) {
            setUpRV(it)
        }

        homeViewModel.loadingStateLiveData.observe(viewLifecycleOwner) {
            onLoadingStateChanged(it)
        }
    }

    private fun initialiseUIElements() {
        binding.goalsAddFirstBtn.setOnClickListener {
            setCurrentFragment(AddGoalCategoryFragment(), "add_category")
        }
        binding.goalsAddBtn.setOnClickListener {
            setCurrentFragment(AddGoalCategoryFragment(), "add_category")
        }
    }

    private fun setUpRV(goalsList: List<Goal>) {
        val goalsAdapter = GoalsAdapter(goalsList)
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
        binding.goalsRV.layoutManager = linearLayoutManager
        binding.goalsRV.adapter = goalsAdapter
        checkEmptyState(goalsList)
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

    private fun onLoadingStateChanged(state: LoadingState) {
        when (state) {
            LoadingState.SUCCESS -> {
                //binding.shimmerLayout.visibility = View.GONE
                //binding.recyclerView.visibility = View.VISIBLE
            }
            LoadingState.LOADING -> {
                //binding.recyclerView.visibility = View.INVISIBLE
                //binding.shimmerLayout.visibility = View.VISIBLE
            }
            LoadingState.ERROR -> {
                //binding.shimmerLayout.visibility = View.GONE
                //binding.recyclerView.visibility = View.VISIBLE
                Toast.makeText(requireContext(), "Error Occurred!", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.fragment, fragment)
            addToBackStack(name)
            commit()
        }
}