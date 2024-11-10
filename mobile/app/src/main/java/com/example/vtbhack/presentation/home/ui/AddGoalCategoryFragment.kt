package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddGoalCategoryBinding

class AddGoalCategoryFragment : Fragment(R.layout.fragment_add_goal_category) {
    private lateinit var binding: FragmentAddGoalCategoryBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentAddGoalCategoryBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        binding.presentBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На подарок"))
        }
        binding.travelBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На путешествие"))
        }
        binding.repairBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На ремонт"))
        }
        binding.medcineBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На медицину"))
        }
        binding.charityBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На благотворительность"))
        }
        binding.addNewBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance("На мечту"))
        }
        binding.closeBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.fragment, fragment)
            addToBackStack(name)
            commit()
        }
}