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
import com.example.vtbhack.databinding.ItemAccountBinding
import com.example.vtbhack.domain.model.AccumulatedAccount

class AccountsAdapter(
    private val accountsList: List<AccumulatedAccount>,
    private val onLinkClicked: (Int) -> Unit
) :
    RecyclerView.Adapter<AccountsAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ItemAccountBinding.bind(itemView)
        val name: TextView
        val amount: TextView
        val link: ImageView

        init {
            name = binding.accountName
            amount = binding.accountAmount
            link = binding.accountLinkBtn
        }

        @RequiresApi(Build.VERSION_CODES.O)
        @SuppressLint("SetTextI18n", "SimpleDateFormat")
        fun bind(model: AccumulatedAccount) {
            name.text = model.account_type
            amount.text = "${model.amount} ${model.currency}"
            link.setOnClickListener {
                onLinkClicked(accountsList.indexOf(model))
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context).inflate(R.layout.item_account, parent, false)
        return ViewHolder(view)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val model: AccumulatedAccount = accountsList[position]
        holder.bind(model)
    }

    override fun getItemCount(): Int {
        return accountsList.size
    }
}