package com.example.vtbhack.presentation.survey.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentFormDepositBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.home.ui.HomeFragment
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModel
import com.example.vtbhack.presentation.survey.viewModel.SurveyViewModelFactory

class FormDepositFragment : Fragment(R.layout.fragment_form_deposit) {
    private lateinit var binding: FragmentFormDepositBinding
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
        binding = FragmentFormDepositBinding.bind(view)

        initialiseObservers()
        initialiseUIElements()
    }

    @SuppressLint("SimpleDateFormat")
    private fun initialiseObservers() {
        surveyViewModel.getRecommendedDeposit(MainActivity.authToken)

        surveyViewModel.recommendedDeposit.observe(viewLifecycleOwner) {
            setUpDeposit(it.recommended_deposit)
        }

        surveyViewModel.loadingStateLiveData.observe(viewLifecycleOwner) {
            onLoadingStateChanged(it)
        }
    }

    private fun initialiseUIElements() {
        binding.closeBtn.setOnClickListener {
            setCurrentFragment(HomeFragment())
        }
    }

    @SuppressLint("SetTextI18n", "DefaultLocale")
    private fun setUpDeposit(deposit: Double) {
        binding.recommendedAmount.text = "${String.format("%.2f", deposit)} руб."
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            commit()
        }

    private fun onLoadingStateChanged(state: LoadingState) {
        when (state) {
            LoadingState.SUCCESS -> {
                binding.circleProgressBar.visibility = View.GONE
                binding.info.visibility = View.VISIBLE
            }
            LoadingState.LOADING -> {
                binding.info.visibility = View.GONE
                binding.circleProgressBar.visibility = View.VISIBLE
            }
            LoadingState.ERROR -> {
                binding.circleProgressBar.visibility = View.GONE
                binding.info.visibility = View.GONE
                Toast.makeText(requireContext(), "Error Occurred!", Toast.LENGTH_LONG).show()
            }
        }
    }
}