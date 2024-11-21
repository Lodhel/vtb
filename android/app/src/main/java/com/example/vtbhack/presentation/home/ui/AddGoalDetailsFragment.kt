package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddGoalDetailsBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val TYPE = "type"
private const val CATEGORY = "category"

class AddGoalDetailsFragment : Fragment(R.layout.fragment_add_goal_details) {
    private lateinit var binding: FragmentAddGoalDetailsBinding
    private var type: String = "Личный"
    private var category: String? = null
    private lateinit var homeViewModel: HomeViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        arguments?.let {
            type = if (it.getString(TYPE) == null) "Личный" else it.getString(TYPE).toString()
            category = it.getString(CATEGORY)
        }

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
        binding = FragmentAddGoalDetailsBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        if (category == "На мечту")
            binding.nameET.isEnabled = true

        binding.nameET.hint = category.toString()

        binding.goalAddBtn.setOnClickListener {

            val description = if (binding.nameET.text.isBlank())
                binding.nameET.hint.toString()
            else
                binding.nameET.text.toString()

            val target_amount = if (binding.amountET.text.isBlank())
                binding.amountET.hint.toString().toDouble()
            else
                binding.amountET.text.toString().toDouble()

            val months_remaining = if (binding.termET.text.isBlank())
                binding.termET.hint.toString().toInt()
            else
                binding.termET.text.toString().toInt()

            homeViewModel.addNewGoal(
                token = MainActivity.authToken,
                type = type,
                description = description,
                target_amount = target_amount,
                months_remaining = months_remaining,
                invitations = true
            )
            requireActivity().supportFragmentManager.popBackStack(
                null,
                FragmentManager.POP_BACK_STACK_INCLUSIVE
            )
            setCurrentFragment(HomeFragment())
        }
        binding.backBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setCurrentFragment(fragment: Fragment) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            commit()
        }

    companion object {
        @JvmStatic
        fun newInstance(type: String?, category: String) =
            AddGoalDetailsFragment().apply {
                arguments = Bundle().apply {
                    putString(TYPE, type)
                    putString(CATEGORY, category)
                }
            }
    }
}