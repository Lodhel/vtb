package com.example.vtbhack.presentation.home.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAccountInfoBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.LoadingState
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.InvitedUser
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val ID = "id"

class AccountInfoFragment : Fragment(R.layout.fragment_account_info) {
    private lateinit var binding: FragmentAccountInfoBinding
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
        binding = FragmentAccountInfoBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseObservers() {
        homeViewModel.accounts.observe(viewLifecycleOwner) {
            setUpRV(it[id].users.invited_users)
        }
    }

    @SuppressLint("SetTextI18n")
    private fun initialiseUIElements() {
        val account = homeViewModel.accounts.value?.get(id)
        binding.title.text = account?.account_type ?: "Накопительный счет"
        binding.ownerName.text = "${account?.users?.owner?.name} ${account?.users?.owner?.lastname}"
        binding.amount.text = "${account?.amount} ${account?.currency}"
        if (account?.users?.invited_users?.isNotEmpty() == true) {
            binding.contactsRV.visibility = View.VISIBLE
            initialiseObservers()
        }
        if (account?.account_type?.equals("Личный") == false && account.users.owner == homeViewModel.currentUser.value) {
            binding.addContact.visibility = View.VISIBLE
            binding.addContact.setOnClickListener {
                setCurrentFragment(AddContactsFragment.newInstance("a$id", "invite", account.id), null)
            }
        }
        binding.closeBtn.setOnClickListener {
            setHomeFragment()
        }
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

    private fun setHomeFragment() =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, HomeFragment())
            commit()
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
            AccountInfoFragment().apply {
                arguments = Bundle().apply {
                    putInt(ID, id)
                }
            }
    }
}