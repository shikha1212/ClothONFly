package com.example.clothonfly

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.squareup.okhttp.MediaType
import kotlinx.android.synthetic.main.loginfragment.*
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.RequestBody
import kotlinx.android.synthetic.main.loginfragment.password
import kotlinx.android.synthetic.main.loginfragment.user_name
import kotlinx.android.synthetic.main.signupfragement.*
import kotlinx.android.synthetic.main.signupfragement.view.*
import kotlinx.android.synthetic.main.signupfragement.view.firstname
import org.jetbrains.anko.doAsync
import org.json.JSONObject
import java.net.URL

/**
 * Fragment representing the login screen for Shrine.
 */

class SignupFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment - all element of the xml is accessible here
        val view = inflater.inflate(R.layout.signupfragement, container, false)

        view.confirm_btn.setOnClickListener {
            doAsync {
                var user_name_var = user_name.text.toString()
                var password_var = password.text.toString()
                var first_name_var = firstname.text.toString()
                var last_name_var = lastname.text.toString()
                var email_var = email.text.toString()
                var address_var = address.text.toString()
                var phone_num_var = phonenum.text.toString()

                val gotresponse =
                    signup_user(user_name_var, password_var, first_name_var,
                        last_name_var, email_var, address_var, phone_num_var)

                val json = JSONObject(gotresponse)
                if (json.get("message") == "Succeeded") {
                    (activity as NavigationHost).navigateTo(LoginFragment(), addToBackstack = false)
                } else {
                    print("Sign up failed!!!")
                }
            }
        }

        view.cancel_btn.setOnClickListener {
            (activity as NavigationHost).navigateTo(LoginFragment(), addToBackstack = false)
        }
        return view
    }

    fun signup_user(user_name: String?, password: String?, first_name: String?,
                    last_name: String?, email: String?, address: String?,
                    phone_num: String?): String {
        val json = """{
        "user_name":"${user_name}",
        "password":"${password}",
        "first_name":"${first_name}",
        "last_name":"${last_name}",
        "email":"${email}",
        "address":"${address}",
        "contact":"${phone_num}"
    }""".trimIndent()

        val url = URL("http://cloth-on-fly.appspot.com/android_signup")
        val client = OkHttpClient()
        val body = RequestBody.create(MediaType.parse("application/json;charset=utf-8"), json)
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        val response = client.newCall(request).execute() //fetches the url from the network - time consuming .
        // if android freezes in this line -check internet coonection and restart your avd
        val bodystr = response.body().string() // this can be consumed only once

        return bodystr
    }

}











