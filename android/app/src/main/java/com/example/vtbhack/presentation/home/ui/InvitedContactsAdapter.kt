package com.example.vtbhack.presentation.home.ui

import android.annotation.SuppressLint
import android.os.Build
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.vtbhack.R
import com.example.vtbhack.databinding.ItemInvitedContactBinding
import com.example.vtbhack.domain.model.InvitedUser

class InvitedContactsAdapter(
    private val contactsList: List<InvitedUser>,
) :
    RecyclerView.Adapter<InvitedContactsAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ItemInvitedContactBinding.bind(itemView)
        val name: TextView
        val role: TextView
        val statusIcon: ImageView

        init {
            name = binding.contactName
            role = binding.role
            statusIcon = binding.status
        }

        @SuppressLint("SetTextI18n")
        fun bind(model: InvitedUser) {
            name.text = "${model.name} ${model.lastname}"
            role.text = model.role
            if (model.status == "ожидает подтверждения") {
                statusIcon.setImageResource(R.drawable.clock)
            }
            else if (model.status == "подтверждено") {
                statusIcon.setImageResource(R.drawable.check)
            }
            else if (model.status == "отклонено") {
                statusIcon.setImageResource(R.drawable.cancel)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context)
                .inflate(R.layout.item_invited_contact, parent, false)
        return ViewHolder(view)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val model: InvitedUser = contactsList[position]
        holder.bind(model)
    }

    override fun getItemCount(): Int {
        return contactsList.size
    }
}