package com.example.vtbhack.presentation.survey.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentFormEducationBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModel
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModelFactory

class FormEducationFragment : Fragment(R.layout.fragment_form_education) {
    private lateinit var binding: FragmentFormEducationBinding
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
        binding = FragmentFormEducationBinding.bind(view)

        initialiseUIElements()
    }

    @SuppressLint("SetTextI18n")
    private fun initialiseUIElements() {
        binding.next.setOnClickListener {
            if (binding.middle.isChecked) {
                surveyViewModel.survey.education = "среднее"
            }
            else if (binding.higher.isChecked) {
                surveyViewModel.survey.education = "высшее"
            }
            else if (binding.postgraduate.isChecked) {
                surveyViewModel.survey.education = "послевузовское"
            }
            setCurrentFragment(FormOccupationFragment())
        }
        binding.backBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            addToBackStack(name)
            commit()
        }
}