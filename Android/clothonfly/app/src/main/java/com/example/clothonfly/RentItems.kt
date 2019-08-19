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
import kotlinx.android.synthetic.main.rent_items.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import java.net.URL
import java.util.ArrayList

class RentItems : Fragment() {

    private var response: String? = null
    private var item: ListView? = null
    private var rentItemModelArrayList: ArrayList<Rent_Item_Model>? = null
    private var rentItemAdapter: RentItemAdapter? = null
    private var user_name_string: String? = null

    override fun onCreateView(    //entry point for the fragment
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.rent_items, container, false)

        item = view.rent_items
        user_name_string = arguments!!["user_name"].toString()

        doAsync {
            try {
                response = loadJSONFromItems(user_name_string)
                // Create a Custom Adapter that gives us a way to "view" each user in the ArrayList
                rentItemModelArrayList = getItemsInfo(response!!)
                // set the order adapter for the userlist viewing
                val handler = Handler(Looper.getMainLooper());
                handler.post({
                    try {
                        rentItemAdapter = RentItemAdapter(view.context, rentItemModelArrayList!!)
                        item!!.adapter = rentItemAdapter
                    } catch (e: Exception){
                        Log.d("Error msg", "error in dealing with the rent item adapter: " + e.toString())
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

        return view
    }

    fun getItemsInfo(response: String): ArrayList<Rent_Item_Model> {
        val rentItemModelArrayList = ArrayList<Rent_Item_Model>()
        try {
            val dataArray = JSONArray(response) // converts to json objects from json strings
            for (i in 0 until dataArray.length()) {                           //the loop converts json objects array to arraylist
                val rentItemsModel = Rent_Item_Model()
                val dataobj = dataArray.getJSONObject(i)
                rentItemsModel.setUserName(user_name_string!!)
                rentItemsModel.setItemID(dataobj.getString("Item_ID"))
                rentItemsModel.setRentalPrice(dataobj.getString("Rental_Price"))
                rentItemModelArrayList.add(rentItemsModel)
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return rentItemModelArrayList
    }

    fun loadJSONFromItems(user_name: String?): String? {  //returns a json string with array of json objects
        val json = """{
        "user_name":"${user_name}"
    }""".trimIndent()

        val url = URL("https://cloth-on-fly.appspot.com/android_buyer_home")
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