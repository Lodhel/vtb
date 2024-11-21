package com.example.vtbhack.presentation.home.ui

import android.os.Build
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.vtbhack.R
import com.example.vtbhack.databinding.ItemContactBinding
import com.example.vtbhack.domain.model.Contact

class ContactsAdapter(
    private val contactsList: List<Contact>,
    private val onContactClick: (Contact) -> Boolean,
    private val isSelected: (Contact) -> Boolean,
) :
    RecyclerView.Adapter<ContactsAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ItemContactBinding.bind(itemView)
        val name: TextView
        val parent: LinearLayout
        val icon: ImageView

        init {
            name = binding.contactName
            parent = binding.parent
            icon = binding.contactIcon
        }

        fun bind(model: Contact) {
            name.text = model.name

            if (!isSelected(model)) {
                icon.setImageResource(R.drawable.person_inactive)
                parent.setBackgroundResource(R.color.base800)
            } else {
                icon.setImageResource(R.drawable.person)
                parent.setBackgroundResource(R.drawable.rounded_light_grey_btn)
            }

            parent.setOnClickListener {
                if (onContactClick(model)) {
                    icon.setImageResource(R.drawable.person_inactive)
                    parent.setBackgroundResource(R.color.base800)
                } else {
                    icon.setImageResource(R.drawable.person)
                    parent.setBackgroundResource(R.drawable.rounded_light_grey_btn)
                }
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context).inflate(R.layout.item_contact, parent, false)
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