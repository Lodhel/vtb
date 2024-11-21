package com.example.vtbhack.presentation.home.ui

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.provider.ContactsContract
import android.view.View
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.widget.SearchView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.vtbhack.MainActivity
import com.example.vtbhack.R
import com.example.vtbhack.databinding.FragmentAddContactsBinding
import com.example.vtbhack.domain.api.ApiHelper
import com.example.vtbhack.domain.api.RetrofitBuilder
import com.example.vtbhack.domain.model.Contact
import com.example.vtbhack.presentation.home.viewModel.HomeViewModel
import com.example.vtbhack.presentation.home.viewModel.HomeViewModelFactory

private const val TYPE = "type"
private const val USECASE = "usecase"
private const val ACCOUNT = "account"

class AddContactsFragment : Fragment(R.layout.fragment_add_contacts) {
    private lateinit var binding: FragmentAddContactsBinding
    private lateinit var homeViewModel: HomeViewModel
    private var type: String? = null
    private var usecase: String = ""
    private var account: Int? = null
    var contactsList: ArrayList<Contact> = ArrayList()
    val phoneNumberRegex =
        ("^((8|\\+7)[\\- ]?)?(\\(?\\d{3}\\)?[\\- ]?)?[\\d\\- ]{7,10}\$").toRegex()

    private val activityResultLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        )
        { permissions ->
            var permissionGranted = true
            permissions.entries.forEach {
                if (it.key in REQUIRED_PERMISSIONS && !it.value)
                    permissionGranted = false
            }
            if (!permissionGranted) {
                Toast.makeText(
                    requireContext(),
                    "Permission request denied",
                    Toast.LENGTH_SHORT
                ).show()
            } else {
                setUpRV(getContactsIntoArrayList())
            }
        }

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

        homeViewModel.clearSelectedContacts()
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding = FragmentAddContactsBinding.bind(view)

        initialiseUIElements()
    }

    private fun initialiseUIElements() {
        if (allPermissionsGranted()) {
            setUpRV(getContactsIntoArrayList())
        } else {
            requestPermissions()
        }

        binding.addNumber.setOnClickListener {
            val number: String = binding.searchView.query.toString()
            val newContact = Contact(number, number)
            contactsList.add(0, newContact)
            homeViewModel.selectedContacts.add(newContact)
            setUpRV(contactsList)
        }
        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener,
            android.widget.SearchView.OnQueryTextListener {

            override fun onQueryTextChange(qString: String): Boolean {
                if (phoneNumberRegex.matches(qString)) {
                    binding.addNumber.setImageResource(R.drawable.add_btn_44)
                    binding.addNumber.isClickable = true
                } else {
                    binding.addNumber.setImageResource(R.drawable.add_btn_44_disabled)
                    binding.addNumber.isClickable = false
                }
                setUpRV(contactsList.filter {
                    it.name.contains(
                        qString,
                        true
                    ) || it.phonenumber.contains(qString)
                })
                return true
            }

            override fun onQueryTextSubmit(qString: String): Boolean {
                return false
            }
        })

        binding.next.setOnClickListener {
            if (homeViewModel.selectedContacts.isNotEmpty())
                setCurrentFragment(AddContactRolesFragment.newInstance(type, usecase, account))
            else if (usecase == "goal") {
                setCurrentFragment(AddGoalCategoryFragment.newInstance(type))
            } else if (usecase == "account") {
                homeViewModel.addNewAccount(token = MainActivity.authToken, type = type ?: "Личный")
                requireActivity().supportFragmentManager.popBackStack(
                    null,
                    FragmentManager.POP_BACK_STACK_INCLUSIVE
                )
                setCurrentFragment(HomeFragment())
            } else if (usecase == "invite") {
                account?.let {
                    homeViewModel.inviteSelectedContacts(MainActivity.authToken, it)
                }
                requireActivity().supportFragmentManager.popBackStack(
                    null,
                    FragmentManager.POP_BACK_STACK_INCLUSIVE
                )
                setCurrentFragment(HomeFragment())
                if (type?.substring(0, 1).equals("g")) {
                    setInfoFragment(GoalInfoFragment.newInstance(type?.substring(1)!!.toInt()))
                } else if (type?.substring(0, 1).equals("a")) {
                    setInfoFragment(AccountInfoFragment.newInstance(type?.substring(1)!!.toInt()))
                }
            }
        }
        binding.backBtn.setOnClickListener {
            requireActivity().onBackPressedDispatcher.onBackPressed()
        }
    }

    private fun setUpRV(contactsList: List<Contact>) {
        val contactsAdapter = ContactsAdapter(contactsList, ::onContactClick, ::isSelected)
        val linearLayoutManager =
            LinearLayoutManager(requireContext(), LinearLayoutManager.VERTICAL, false)
        binding.contactsRV.layoutManager = linearLayoutManager
        binding.contactsRV.adapter = contactsAdapter
    }

    private fun isSelected(contact: Contact): Boolean = contact in homeViewModel.selectedContacts

    private fun onContactClick(contact: Contact): Boolean {
        if (contact in homeViewModel.selectedContacts) {
            homeViewModel.selectedContacts.remove(contact)
            checkEmptySelectedList()
            return true
        }
        homeViewModel.selectedContacts.add(contact)
        checkEmptySelectedList()
        return false
    }

    private fun checkEmptySelectedList() {
        if (homeViewModel.selectedContacts.isEmpty()) {
            binding.next.text = "Готово"
            binding.next.setBackgroundResource(R.drawable.rounded_light_blue_btn)
            binding.next.setTextColor(Color.parseColor("#FFFFFF"))
        } else {
            binding.next.text = "Далее"
            binding.next.setBackgroundResource(R.drawable.rounded_blue_btn)
            binding.next.setTextColor(Color.parseColor("#2E8AFF"))
        }
    }

    private fun setCurrentFragment(fragment: Fragment, name: String? = null) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            addToBackStack(name)
            commit()
        }

    private fun setInfoFragment(fragment: Fragment) =
        requireActivity().supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            addToBackStack(null)
            commit()
        }

    @SuppressLint("Range")
    fun getContactsIntoArrayList(): ArrayList<Contact> {
        val cursor =
            requireActivity().contentResolver.query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                null, null, null, null
            )

        while (cursor!!.moveToNext()) {
            val name =
                cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME))
            val phonenumber =
                cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER))
            contactsList.add(Contact(name, phonenumber))
        }

        cursor.close()

        contactsList = contactsList.distinct() as ArrayList<Contact>
        contactsList.sortBy { it.name }
        return contactsList
    }

    private fun requestPermissions() {
        activityResultLauncher.launch(REQUIRED_PERMISSIONS)
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(
            requireContext(), it
        ) == PackageManager.PERMISSION_GRANTED
    }

    companion object {
        @JvmStatic
        fun newInstance(type: String?, usecase: String, account: Int?) =
            AddContactsFragment().apply {
                arguments = Bundle().apply {
                    putString(TYPE, type)
                    putString(USECASE, usecase)
                    if (account != null) {
                        putInt(ACCOUNT, account)
                    }
                }
            }

        private val REQUIRED_PERMISSIONS =
            mutableListOf(
                Manifest.permission.READ_CONTACTS
            ).toTypedArray()
    }

}