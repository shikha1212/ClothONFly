package com.example.clothonfly

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ListView
import androidx.fragment.app.Fragment
import com.squareup.okhttp.MediaType
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.RequestBody
import kotlinx.android.synthetic.main.my_orders.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import java.net.URL
import java.util.ArrayList

class MyOrders : Fragment() {

    private var response: String? = null
    private var order: ListView? = null
    private var orderModelArrayList: ArrayList<Order_Model>? = null
    private var orderAdapter: OrderAdapter? = null
    private var user_name_string: String? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        val view = inflater.inflate(R.layout.my_orders, container, false)
        order = view.orders
//        user_name_string = arguments!!["user_name"].toString()
        user_name_string = Global.getUserName()

        doAsync {
            try {
                response = loadJSONFromOrders(user_name_string)
                // Create a Custom Adapter that gives us a way to "view" each user in the ArrayList
                orderModelArrayList = getOrdersInfo(response!!)
                // set the order adapter for the userlist viewing
                val handler = Handler(Looper.getMainLooper());
                handler.post({
                    try {
                        orderAdapter = OrderAdapter(view.context, orderModelArrayList!!)
                        order!!.adapter = orderAdapter
                    } catch (e: Exception){
                        Log.d("Error msg", "error in dealing with the order adapter: " + e.toString())
                    }
                })
            } catch (e: Exception) {
                println("error in doasync" + e.toString())
            } finally {
            }
        }

        view.home_button.setOnClickListener {
            doAsync {
                (activity as NavigationHost).navigateTo(BuyerHome().apply {
                    arguments = Bundle(1).apply {
                        putString("user_name", user_name_string)
                    }
                }, addToBackstack = false)
            }
        }

        view.refresh_button.setOnClickListener {
            fragmentManager!!.beginTransaction().detach(this).attach(this).commit()
        }

        view.logout_button.setOnClickListener {
            doAsync {
                (activity as NavigationHost).navigateTo(LoginFragment(), addToBackstack = false)
            }
        }

        return view;
    }

    fun getOrdersInfo(response: String): ArrayList<Order_Model> {
        val orderModelArrayList = ArrayList<Order_Model>()
        try {
            val dataArray = JSONArray(response) // converts to json objects from json strings
            for (i in 0 until dataArray.length()) {                           //the loop converts json objects array to arraylist
                val orderModel = Order_Model()
                val dataobj = dataArray.getJSONObject(i)
                orderModel.setOrderId(dataobj.getString("Order_ID"))
                orderModel.setOrderStatus(dataobj.getString("Order_Status"))
                orderModel.setItemId(dataobj.getString("Item_ID"))
                orderModel.setDeliveryDate(dataobj.getString("Delivery_Date"))
                orderModel.setReturnDate(dataobj.getString("Return_Date"))
                orderModel.setActualReturnDate(dataobj.getString("Actual_Return_Date"))
                orderModel.setShippingAddress(dataobj.getString("Shipping_Address"))
                orderModel.setShippingDate(dataobj.getString("Shipping_Date"))
                orderModelArrayList.add(orderModel)
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return orderModelArrayList
    }

    fun loadJSONFromOrders(user_name: String?): String? {  //returns a json string with array of json objects

        val json = """{
        "user_name":"${user_name}"
    }""".trimIndent()

        val url = URL("https://cloth-on-fly.appspot.com/android_myorders")
        val client = OkHttpClient()
        val body = RequestBody.create(MediaType.parse("application/json;charset=utf-8"), json)
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        val response = client.newCall(request).execute() //fetches the url from the network - time consuming .

        val bodystr = response.body().string() // this can be consumed only once
        return bodystr
    }
}