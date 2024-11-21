package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddAccountTypeBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val USECASE = "usecase"

class AddAccountTypeFragment : Fragment(R.layout.fragment_add_account_type) {
    private lateinit var binding: FragmentAddAccountTypeBinding
    private lateinit var homeViewModel: HomeViewModel
    private var usecase: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        homeViewModel = ViewModelProvider(
            requireActivity(), HomeViewModelFactory(
                ApiHelper(
                    RetrofitBuilder.apiService
                )
            )
        )[HomeViewModel::class.java]

        arguments?.let {
            usecase = it.getString(USECASE).toString()
        }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentAddAccountTypeBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        binding.personalBtn.setOnClickListener {
            homeViewModel.addNewAccount(MainActivity.authToken)
            requireActivity().supportFragmentManager.beginTransaction().apply {
                replace(R.id.mainFragment, HomeFragment())
                commit()
            }
        }
        binding.jointBtn.setOnClickListener {
            setCurrentFragment(AddContactsFragment.newInstance("Совместный", usecase, null))
        }
        binding.childBtn.setOnClickListener {
            setCurrentFragment(AddContactsFragment.newInstance("Счет для детей", usecase, null))
        }
        binding.crowdBtn.setOnClickListener {
            setCurrentFragment(AddContactsFragment.newInstance("Краудфандинг", usecase, null))
        }
        binding.investmentsBtn.setOnClickListener {
            setCurrentFragment(AddContactsFragment.newInstance("Инвестиционный", usecase, null))
        }
        binding.socialBtn.setOnClickListener {
            setCurrentFragment(AddContactsFragment.newInstance("Социальный", usecase, null))
        }
        binding.closeBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
        binding.closeBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            addToBackStack(name)
            commit()
        }

    companion object {
        @JvmStatic
        fun newInstance(usecase: String) =
            AddAccountTypeFragment().apply {
                arguments = Bundle().apply {
                    putString(USECASE, usecase)
                }
            }
    }
}