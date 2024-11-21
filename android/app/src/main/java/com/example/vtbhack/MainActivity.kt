package com.example.vtbhack

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.example.vtbhack.databinding.ActivityMainBinding
import com.example.vtbhack.presentation.home.ui.HomeFragment

class MainActivity : AppCompatActivity() {
    private lateinit var viewBinding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewBinding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(viewBinding.root)
        setCurrentFragment(HomeFragment.newInstance())
    }

    private fun setCurrentFragment(fragment: Fragment) =
        supportFragmentManager.beginTransaction().apply {
            replace(R.id.mainFragment, fragment)
            commit()
        }

    companion object {
        val authToken = "VTBAuthToken16"
    }
}