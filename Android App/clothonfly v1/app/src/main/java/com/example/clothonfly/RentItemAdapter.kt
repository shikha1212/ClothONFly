package com.example.clothonfly


import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import com.squareup.okhttp.MediaType
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.RequestBody
import kotlinx.android.synthetic.main.available_items.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONObject
import java.net.URL
import java.util.ArrayList

/**
 * Orignial author: Parsania Hardik on 03-Jan-17.
 * Modified by Ramesh Yerraballi on 8/12/19
 */
class RentItemAdapter(private val context: Context, private val rentItemModelArrayList: ArrayList<Rent_Item_Model>) :
    BaseAdapter() {

    override fun getViewTypeCount(): Int {
        return count
    }

    override fun getItemViewType(position: Int): Int {

        return position
    }

    override fun getCount(): Int {
        return rentItemModelArrayList.size
    }

    override fun getItem(position: Int): Any {
        return rentItemModelArrayList[position]
    }

    override fun getItemId(position: Int): Long {
        return 0
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        var convertView = convertView
        val holder: ViewHolder

        if (convertView == null) {
            holder = ViewHolder()
            val inflater = context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            convertView = inflater.inflate(R.layout.available_items, null, true)

            holder.item_id = convertView!!.findViewById(R.id.item_id) as TextView
            holder.rental_price = convertView.findViewById(R.id.rental_price) as TextView

            convertView.tag = holder

            convertView.rent_button.setOnClickListener {
                doAsync {

                    var rent_days = convertView.rent_days.text.toString()
                    var shipping_address = convertView.shipping_address.text.toString()
                    var response = rent_item(rentItemModelArrayList[position].getUserName(), rentItemModelArrayList[position].getItemID(),
                        rentItemModelArrayList[position].getRentalPrice(), rent_days, shipping_address)

                    val json = JSONObject(response)
                    if (json.get("message") == "Succeeded") {
                        // TODO
                    } else {
                        Log.d("Refresh failed", "Failed to refresh the scroll listing view\n")
                    }
                }
            }
        } else {
            // the getTag returns the viewHolder object set as a tag to the view
            holder = convertView.tag as ViewHolder
        }

        holder.item_id!!.text = "Item ID: " + rentItemModelArrayList[position].getItemID()
        holder.rental_price!!.text = "Rental Price: " + rentItemModelArrayList[position].getRentalPrice()

        return convertView
    }

    fun rent_item(user_name: String?, item_Id: String?, rental_price: String?,
                  rent_days: String?, shipping_address: String?): String {
        val json = """{
        "User_Name":"${user_name}",
        "Item_ID":"${item_Id}",
        "Rental_Price":"${rental_price}",
        "Rent_Days":"${rent_days}",
        "Shipping_Address":"${shipping_address}"
    }""".trimIndent()

        val url = URL("http://cloth-on-fly.appspot.com/android_rent_item")
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

    private inner class ViewHolder {

        var item_id: TextView? = null
        var rental_price: TextView? = null
    }

}