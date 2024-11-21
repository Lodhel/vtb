package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddGoalCategoryBinding

private const val TYPE = "type"

class AddGoalCategoryFragment : Fragment(R.layout.fragment_add_goal_category) {
    private lateinit var binding: FragmentAddGoalCategoryBinding
    private var type: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        arguments?.let {
            type = it.getString(TYPE)
        }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentAddGoalCategoryBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        binding.presentBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На подарок"))
        }
        binding.travelBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На путешествие"))
        }
        binding.repairBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На ремонт"))
        }
        binding.medcineBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На медицину"))
        }
        binding.charityBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На благотворительность"))
        }
        binding.addNewBtn.setOnClickListener {
            setCurrentFragment(AddGoalDetailsFragment.newInstance(type, "На мечту"))
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

    companion object {
        @JvmStatic
        fun newInstance(type: String?) =
            AddGoalCategoryFragment().apply {
                arguments = Bundle().apply {
                    putString(TYPE, type)
                }
            }
    }
}