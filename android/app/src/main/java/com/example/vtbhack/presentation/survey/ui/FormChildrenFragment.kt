package com.example.vtbhack.presentation.survey.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentFormChildrenBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModel
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModelFactory

class FormChildrenFragment : Fragment(R.layout.fragment_form_children) {
    private lateinit var binding: FragmentFormChildrenBinding
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
        binding = FragmentFormChildrenBinding.bind(view)

        initialiseUIElements()
    }

    @SuppressLint("SetTextI18n")
    private fun initialiseUIElements() {
        binding.next.setOnClickListener {
            surveyViewModel.survey.children_count = if (binding.childrenET.text.toString() == "") {
                binding.childrenET.hint.toString().toInt()
            } else {
                binding.childrenET.text.toString().toInt()
            }
            setCurrentFragment(FormEducationFragment())
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