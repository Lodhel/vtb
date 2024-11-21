package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddProductTypeBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory


class AddProductTypeFragment : Fragment(R.layout.fragment_add_product_type) {
    private lateinit var binding: FragmentAddProductTypeBinding
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
        binding = FragmentAddProductTypeBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        binding.next.setOnClickListener {
            if (binding.account.isChecked) {
                setCurrentFragment(AddAccountTypeFragment.newInstance("account"))
            }
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
        fun newInstance() = AddProductTypeFragment()
    }
}