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
import kotlinx.android.synthetic.main.loginfragment.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONObject
import java.net.URL

/**
 * Fragment representing the login screen for Shrine.
 */

class LoginFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment - all element of the xml is accessible here
        val view = inflater.inflate(R.layout.loginfragment, container, false)
        // Set an error if the password is less than 8 characters.
        view.login_button.setOnClickListener {
            doAsync {
                var user_name_var = user_name.text.toString()
                var password_var = password.text.toString()

                val gotresponse =
                    validate_user(user_name_var, password_var)
                val json = JSONObject(gotresponse)
                    if (json.get("role") == "Buyer") {
                        (activity as NavigationHost).navigateTo(BuyerHome().apply {
                            arguments = Bundle(1).apply {
                                putString("user_name", user_name_var)
                            }
                        }, addToBackstack = false)
//                            user_name.setText("Buyer")
                    } else {
                        user_name.setText("")
                        password.setText("")
                }
            }
        }

        view.signup_button.setOnClickListener {
            doAsync {
                (activity as NavigationHost).navigateTo(SignupFragment(), addToBackstack = false)
            }
        }

        return view
    }

    fun validate_user(user_name: String?, password: String?): String {
        val json = """{
        "username":"${user_name}",
        "password":"${password}"
    }""".trimIndent()
        val url = URL("http://cloth-on-fly.appspot.com/validate_user")
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











