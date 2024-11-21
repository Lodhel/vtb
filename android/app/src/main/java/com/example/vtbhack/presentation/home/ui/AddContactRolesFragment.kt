package com.example.vtbhack.presentation.home.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddContactRolesBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.Contact
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val TYPE = "type"
private const val USECASE = "usecase"
private const val ACCOUNT = "account"

class AddContactRolesFragment : Fragment(R.layout.fragment_add_contact_roles) {
    private lateinit var binding: FragmentAddContactRolesBinding
    private lateinit var homeViewModel: HomeViewModel
    private var type: String? = null
    private var usecase: String = ""
    private var account: Int? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        arguments?.let {
            type = it.getString(TYPE) ?: "Личный"
            usecase = it.getString(USECASE).toString()
            account = it.getInt(ACCOUNT)
        }

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
        binding = FragmentAddContactRolesBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        setUpRV(homeViewModel.selectedContacts)

        binding.next.setOnClickListener {
            if (usecase == "goal") {
                setCurrentFragment(AddGoalCategoryFragment.newInstance(type))
            }
            else if (usecase == "account") {
                homeViewModel.addNewAccount(token = MainActivity.authToken, type = type ?: "Личный", invitations = true)
                requireActivity().supportFragmentManager.popBackStack(
                    null,
                    FragmentManager.POP_BACK_STACK_INCLUSIVE
                )
                setCurrentFragment(HomeFragment())
            }
            else if (usecase == "invite") {
                account?.let {
                    homeViewModel.inviteSelectedContacts(MainActivity.authToken, it)
                }
                requireActivity().supportFragmentManager.popBackStack(
                    null,
                    FragmentManager.POP_BACK_STACK_INCLUSIVE
                )
                if (type?.substring(0, 1).equals("g")) {
                    setCurrentFragment(GoalInfoFragment.newInstance(type?.substring(1)!!.toInt()))
                }
                else if (type?.substring(0, 1).equals("a")) {
                    setCurrentFragment(AccountInfoFragment.newInstance(type?.substring(1)!!.toInt()))
                }
            }
        }
        binding.backBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setUpRV(contactsList: List<Contact>) {
        val contactsAdapter = ContactRolesAdapter(
            contactsList,
            requireContext(),
            resources.getStringArray(R.array.contactRoles),
            ::changeRole
        )
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.VERTICAL, false)
        binding.contactRolesRV.layoutManager = linearLayoutManager
        binding.contactRolesRV.adapter = contactsAdapter
    }

    private fun changeRole(contact: Contact, s: String) {
        val id = homeViewModel.selectedContacts.indexOf(contact)
        homeViewModel.selectedContacts[id] = contact.copy(role = s)
    }

    private fun setCurrentFragment(fragment: Fragment) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            commit()
        }

    companion object {
        @JvmStatic
        fun newInstance(type: String?, usecase: String, account: Int?) =
            AddContactRolesFragment().apply {
                arguments = Bundle().apply {
                    putString(TYPE, type)
                    putString(USECASE, usecase)
                    if (account != null) {
                        putInt(ACCOUNT, account)
                    }
                }
            }
    }
}