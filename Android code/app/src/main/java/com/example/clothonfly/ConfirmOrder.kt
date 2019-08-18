package com.example.clothonfly

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ListView
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.clothonfly.CustomAdapter
import com.example.clothonfly.Item_Model
import com.example.clothonfly.R
import com.squareup.okhttp.MediaType
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.RequestBody
import kotlinx.android.synthetic.main.confirm_order.*
import kotlinx.android.synthetic.main.confirm_order.address
import kotlinx.android.synthetic.main.confirm_order.itemid
//import kotlinx.android.synthetic.main.confirm_order.price
import kotlinx.android.synthetic.main.confirm_order.view.*
import kotlinx.android.synthetic.main.loginfragment.*
import kotlinx.android.synthetic.main.loginfragment.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.net.URL
import java.util.ArrayList
import android.widget.TextView
import android.graphics.BitmapFactory
import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import kotlinx.android.synthetic.main.buyer_home.view.*
import java.io.InputStream


class ConfirmOrder : Fragment() {

    override fun onCreateView(    //entry point for the fragment
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.confirm_order, container, false)
        doAsync {

            try{
                val text = view.findViewById(R.id.itemid) as TextView
            text.text = Global.get_itemid()

            val handler = Handler(Looper.getMainLooper());
            handler.post({
                try {
                    val imageUrl ="https://cloth-on-fly.appspot.com/look/" + Global.getimg()
                    Glide.with(context).load(imageUrl).into(imageView2)

                } catch (e: Exception){
                }
            })
        } catch (e: Exception) {
            println("error in doasync" + e.toString())
        } finally {
        }





        }



        val item_id_var = Global.get_itemid()
        val user = Global.getUserName()
        view.btn_calculate_price.setOnClickListener {
            doAsync {
                var days_var = days.text.toString()
                val gotresponse = calculate_price(item_id_var, days_var)
                val json = JSONObject(gotresponse)
                val totalprice = json.get("price").toString()
                finalprice.setText(totalprice)
                Global.setprice(totalprice)
                Global.setdays(days_var)

            }
        }
//
                view.btn_place_order.setOnClickListener {
                    doAsync {
                        val user_name = Global.getUserName()
                        var days = days.text.toString()
                        val shippingaddress = address.text.toString()
                        val gotresponse = place_order(item_id_var, user_name, days, shippingaddress)
                        val json = JSONObject(gotresponse)
                        val order = json.get("order_id").toString()
                        (activity as NavigationHost).navigateTo(MyOrders(), addToBackstack = false)

                    }
                }

        view.btn_cancel_order.setOnClickListener({
            // Navigate to the Confirm Order Fragment.
            (activity as NavigationHost).navigateTo(BuyerHome(), addToBackstack = false) // addtoBackstack : false disables back button
        })



        return view
        }





    fun calculate_price(item_id: String?, days: String?): String {
        val json = """{
        "item_id":"${item_id}",
        "days":"${days}"
    }""".trimIndent()
        val url = URL("http://cloth-on-fly.appspot.com/android_calculate_price")
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

    fun place_order(item_id: String?, user_name: String?,days: String?,shippingaddress: String?): String {
        val json = """{
        "item_id":"${item_id}",
        "user_name":"${user_name}",
        "days" : "${days}",
        "shippingaddress" :"${shippingaddress}"
    }""".trimIndent()
        val url = URL("http://cloth-on-fly.appspot.com/android_place_order")
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