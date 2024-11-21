package com.example.vtbhack.presentation.home.ui

import android.annotation.SuppressLint
import android.os.Build
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.ProgressBar
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.vtbhack.R
import com.example.vtbhack.databinding.ItemGoalBinding
import com.example.vtbhack.domain.model.Goal
import java.text.SimpleDateFormat

class GoalsAdapter(
    private val goalsList: List<Goal>,
    private val onGoalClicked: (Int) -> Unit
) :
    RecyclerView.Adapter<GoalsAdapter.ViewHolder>() {

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ItemGoalBinding.bind(itemView)
        val title: TextView
        val progressBar: ProgressBar
        val progressSum: TextView
        val adviceSum: TextView
        val adviceText: TextView
        val jointImage: ImageView
        val openBtn: ImageView

        init {
            title = binding.goalTitle
            progressBar = binding.progressBar
            progressSum = binding.progressSum
            adviceSum = binding.adviceSum
            adviceText = binding.adviceText
            jointImage = binding.jointImage
            openBtn = binding.openGoalBtn
        }

        @RequiresApi(Build.VERSION_CODES.O)
        @SuppressLint("SetTextI18n", "SimpleDateFormat")
        fun bind(model: Goal) {
            title.text = model.description
            progressBar.progress = model.progress_percentage.toInt()
            progressSum.text = (model.target_amount / 100 * model.progress_percentage).toInt().toString()
            adviceSum.text = "${model.recommended_contribution.toInt()} р"
            val sdf = SimpleDateFormat("yyyy-MM-dd")
            val date = sdf.parse(model.rate_date)
            val rateDateFormatted: String = SimpleDateFormat("dd.MM.yyyy").format(date)
            adviceText.text =
                "Рекомендуемый платеж для достижения цели в срок до $rateDateFormatted"
            if (model.joint)
                jointImage.visibility = View.VISIBLE
            else
                jointImage.visibility = View.GONE
            openBtn.setOnClickListener {
                onGoalClicked(goalsList.indexOf(model))
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context).inflate(R.layout.item_goal, parent, false)
        return ViewHolder(view)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val model: Goal = goalsList[position]
        holder.bind(model)
    }

    override fun getItemCount(): Int {
        return goalsList.size
    }
}