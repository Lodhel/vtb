package com.example.vtbhack

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.vtbhack.databinding.ActivityMainBinding
import com.example.vtbhack.presentation.home.ui.HomeActivity

class MainActivity : AppCompatActivity() {
    private lateinit var viewBinding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewBinding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(viewBinding.root)

        startActivity(HomeActivity.newIntent(this))
    }
}