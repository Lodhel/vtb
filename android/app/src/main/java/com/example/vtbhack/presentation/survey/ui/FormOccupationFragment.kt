package com.example.vtbhack.presentation.survey.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentFormOccupationBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModel
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModelFactory

class FormOccupationFragment : Fragment(R.layout.fragment_form_occupation) {
    private lateinit var binding: FragmentFormOccupationBinding
    private lateinit var surveyViewModel: SurveyViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        surveyViewModel = ViewModelProvider(
            requireActivity(), SurveyViewModelFactory(
                ApiHelper(
                    RetrofitBuilder.apiService
                )
            )
        )[SurveyViewModel::class.java]
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentFormOccupationBinding.bind(view)

        initialiseUIElements()
    }

    @SuppressLint("SetTextI18n")
    private fun initialiseUIElements() {
        binding.next.setOnClickListener {
            if (binding.privateCompany.isChecked) {
                surveyViewModel.survey.occupation = "работник частной компании"
            }
            else if (binding.freelance.isChecked) {
                surveyViewModel.survey.occupation = "самозанятый"
            }
            else if (binding.stateCompany.isChecked) {
                surveyViewModel.survey.occupation = "госслужащий"
            }
            surveyViewModel.postSurvey(MainActivity.authToken)
            requireActivity().supportFragmentManager.popBackStack(
                null,
                FragmentManager.POP_BACK_STACK_INCLUSIVE
            )
            setCurrentFragment(FormDepositFragment())
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
}