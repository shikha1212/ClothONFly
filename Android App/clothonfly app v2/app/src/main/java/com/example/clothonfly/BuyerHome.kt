package com.example.clothonfly

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ListView
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.buyer_home.view.*
import kotlinx.android.synthetic.main.buyer_home.view.*
import kotlinx.android.synthetic.main.loginfragment.*
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.net.URL
import java.util.ArrayList
//import androidx.test.internal.runner.junit4.statement.UiThreadStatement.runOnUiThread
import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.activityUiThread


class BuyerHome : Fragment() {
    private val jsoncode = 1
    private var response: String? = null
    private var item:ListView? = null
    private var ItemArrayList: ArrayList<String>? = null
    private var ItemModelArrayList: ArrayList<Item_Model>? = null
    private var customAdapter: CustomAdapter? = null

    override fun onCreateView(    //entry point for the fragment
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.buyer_home, container, false)
        item = view.items //declare a local variable and initialize to what we get from xml
//        userModelArrayList = getInfo(response)  // uncomment this and comment the next line if response is above

            doAsync {
                try {
                    response = loadJSONFromItems()
                    // Create a Custom Adapter that gives us a way to "view" each user in the ArrayList
                    ItemModelArrayList = getInfo(response!!)
                    // set the custom adapter for the userlist viewing
                    val handler = Handler(Looper.getMainLooper());
                    handler.post({
                        try {
                            customAdapter = CustomAdapter(view.context, ItemModelArrayList!!)
                            item!!.adapter = customAdapter

                        } catch (e: Exception){
                        }
                    })
                } catch (e: Exception) {
                    println("error in doasync" + e.toString())
                } finally {
                }
            }


        view.rent_button.setOnClickListener({
            // Navigate to the Confirm Order Fragment.
            (activity as NavigationHost).navigateTo(ConfirmOrder(), addToBackstack = false) // addtoBackstack : false disables back button
        })

        view.logout_button.setOnClickListener({
            // Navigate to the Confirm Order Fragment.
            (activity as NavigationHost).navigateTo(LoginFragment(), addToBackstack = false) // addtoBackstack : false disables back button
        })

        view.myorders_button.setOnClickListener({
            // Navigate to the Confirm Order Fragment.
            (activity as NavigationHost).navigateTo(MyOrders(), addToBackstack = false) // addtoBackstack : false disables back button
        })


        return view;
    }

    fun getInfo(response: String): ArrayList<Item_Model> {
        val itemModelArrayList = ArrayList<Item_Model>()
        try {
//            val json = JSONObject(response)
            val dataArray = JSONArray(response) // converts to json objects from json strings
            for (i in 0 until dataArray.length()) {                           //the loop converts json objects array to arraylist
                val itemsModel = Item_Model()
                val dataobj = dataArray.getJSONObject(i)
                itemsModel.setID(dataobj.getString("Item_ID"))
                itemsModel.setRentalPrice(dataobj.getString("Rental_Price"))
                itemsModel.setOriginalPrice(dataobj.getString("Original_Price"))
                itemsModel.setdeposit(dataobj.getString("Deposit"))
                itemsModel.setbrand(dataobj.getString("Brand_Name"))
                itemsModel.setsize(dataobj.getString("Size"))
                itemsModel.setimage(dataobj.getString("Cloth_Image"))
                itemModelArrayList.add(itemsModel)
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return itemModelArrayList
    }

    fun loadJSONFromItems(): String? {  //returns a json string with array of json objects
        val url = URL("https://cloth-on-fly.appspot.com/android_buyer_home")
        val client = OkHttpClient()
//        val body = null
        val request = Request.Builder()
            .url(url)
            .build()

        val response = client.newCall(request).execute() //fetches the url from the network - time consuming .
        // if android freezes in this line -check internet coonection and restart your avd

        val bodystr = response.body().string() // this can be consumed only once
        return bodystr

    }

    fun getStrings(response: String): ArrayList<String> {
        val userArrayList = ArrayList<String>()
        try {
            val dataArray = JSONArray(response)
            for (i in 0 until dataArray.length()) {
                val dataobj = dataArray.getJSONObject(i)
                userArrayList.add(dataobj.toString())
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return userArrayList
    }
}

