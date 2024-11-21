package com.example.vtbhack.presentation.home.ui

import android.content.Context
import android.os.Build
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Spinner
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.vtbhack.R
import com.example.vtbhack.databinding.ItemContactRoleBinding
import com.example.vtbhack.domain.model.Contact


class ContactRolesAdapter(
    private val contactsList: List<Contact>,
    private val context: Context,
    private val rolesArray: Array<String>,
    private val changeRole: (Contact, String) -> Unit
) :
    RecyclerView.Adapter<ContactRolesAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ItemContactRoleBinding.bind(itemView)
        val name: TextView
        val spinner: Spinner

        init {
            name = binding.contactName
            spinner = binding.roleSpinner
        }

        fun bind(model: Contact) {
            name.text = model.name

            val spinnerAdapter = ArrayAdapter<String>(context, R.layout.layout_spinner, rolesArray)
            spinner.adapter = spinnerAdapter
            spinner.setSelection(rolesArray.indexOf(model.role))
            spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(
                    parentView: AdapterView<*>?,
                    selectedItemView: View?,
                    position: Int,
                    id: Long
                ) {
                    changeRole(model, rolesArray[position])
                }

                override fun onNothingSelected(parentView: AdapterView<*>?) { }
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context).inflate(R.layout.item_contact_role, parent, false)
        return ViewHolder(view)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val model: Contact = contactsList[position]
        holder.bind(model)


    }

    override fun getItemCount(): Int {
        return contactsList.size
    }
}