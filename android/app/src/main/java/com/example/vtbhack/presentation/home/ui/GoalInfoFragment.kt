package com.example.vtbhack.presentation.home.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentGoalInfoBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.InvitedUser
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val ID = "id"

class GoalInfoFragment : Fragment(R.layout.fragment_goal_info) {
    private lateinit var binding: FragmentGoalInfoBinding
    private lateinit var homeViewModel: HomeViewModel
    private var id: Int = 0

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
            id = it.getInt(ID)
        }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentGoalInfoBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseObservers() {
        homeViewModel.accounts.observe(viewLifecycleOwner) {
            setUpRV(it[id].users.invited_users)
        }
    }

    @SuppressLint("SetTextI18n")
    private fun initialiseUIElements() {
        val goal = homeViewModel.goals.value?.get(id)
        val account = homeViewModel.accounts.value?.get(id)
        binding.ownerName.text = "${account?.users?.owner?.name} ${account?.users?.owner?.lastname}"
        binding.title.text = goal?.description ?: "Копилка"
        goal?.progress_percentage?.let { binding.progressBar.progress = it.toInt() }
        if (goal != null) {
            binding.amount.text =
                "${(goal.target_amount / 100 * goal.progress_percentage).toInt()} из ${goal.target_amount} ${account?.currency}"
        }
        if (account?.users?.invited_users?.isNotEmpty() == true) {
            binding.contactsRV.visibility = View.VISIBLE
            initialiseObservers()
        }
        if (account?.account_type?.equals("Личный") == false && account.users.owner == homeViewModel.currentUser.value) {
            binding.addContact.visibility = View.VISIBLE
            binding.addContact.setOnClickListener {
                setCurrentFragment(
                    AddContactsFragment.newInstance("g$id", "invite", account.id), null)
            }
        }
        binding.closeBtn.setOnClickListener {
            setCurrentFragment(HomeFragment())
        }
    }

    private fun setCurrentFragment(fragment: Fragment) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            commit()
        }

    private fun setUpRV(contactsList: List<InvitedUser>) {
        val contactsAdapter = InvitedContactsAdapter(contactsList)
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.VERTICAL, false)
        binding.contactsRV.layoutManager = linearLayoutManager
        binding.contactsRV.adapter = contactsAdapter
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
            replace(R.id.mainFragment, fragment)
            addToBackStack(name)
            commit()
        }

    companion object {
        @JvmStatic
        fun newInstance(id: Int) =
            GoalInfoFragment().apply {
                arguments = Bundle().apply {
                    putInt(ID, id)
                }
            }
    }
}