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
import kotlinx.android.synthetic.main.order_items.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONObject
import java.net.URL
import java.util.ArrayList

/**
 * Orignial author: Parsania Hardik on 03-Jan-17.
 * Modified by Ramesh Yerraballi on 8/12/19
 */
class OrderAdapter(private val context: Context, private val orderModelArrayList: ArrayList<Order_Model>) :
    BaseAdapter() {

    override fun getViewTypeCount(): Int {
        return count
    }

    override fun getItemViewType(position: Int): Int {

        return position
    }

    override fun getCount(): Int {
        return orderModelArrayList.size
    }

    override fun getItem(position: Int): Any {
        return orderModelArrayList[position]
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
            convertView = inflater.inflate(R.layout.order_items, null, true)

            holder.order_id = convertView!!.findViewById(R.id.order_id) as TextView
            holder.order_status = convertView.findViewById(R.id.order_status) as TextView
            holder.item_id = convertView!!.findViewById(R.id.item_id) as TextView
            holder.delivery_date = convertView.findViewById(R.id.delivery_date) as TextView
            holder.return_date = convertView!!.findViewById(R.id.return_date) as TextView
            holder.actual_return_date = convertView.findViewById(R.id.actual_return_date) as TextView
            holder.shipping_address = convertView!!.findViewById(R.id.shipping_address) as TextView
            holder.shipping_date = convertView.findViewById(R.id.shipping_date) as TextView

            convertView.tag = holder

            convertView.return_button.setOnClickListener {
                doAsync {
                    var response = return_item(orderModelArrayList[position].getOrderId(),orderModelArrayList[position].getItemId())
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

        holder.order_id!!.text = "Order ID: " + orderModelArrayList[position].getOrderId()
        holder.order_status!!.text = "Order Status: " + orderModelArrayList[position].getOrderStatus()
        holder.item_id!!.text = "Item ID: " + orderModelArrayList[position].getItemId()
        holder.delivery_date!!.text = "Delivery Date: " + orderModelArrayList[position].getDeliveryDate()
        holder.return_date!!.text = "Return Date: " + orderModelArrayList[position].getReturnDate()
        holder.actual_return_date!!.text = "Actual Return Date: " + orderModelArrayList[position].getActualReturnDate()
        holder.shipping_address!!.text = "Shipping Address: " + orderModelArrayList[position].getShippingAddress()
        holder.shipping_date!!.text = "Shipping Date: " + orderModelArrayList[position].getShippingDate()

        return convertView
    }

    fun return_item(order_Id: String?, item_Id: String?): String {
        val json = """{
        "Order_ID":"${order_Id}",
        "Item_ID":"${item_Id}"
    }""".trimIndent()

        val url = URL("http://cloth-on-fly.appspot.com/android_return_item")
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

        var order_id: TextView? = null
        var order_status: TextView? = null
        var item_id: TextView? = null
        var delivery_date: TextView? = null
        var return_date: TextView? = null
        var actual_return_date: TextView? = null
        var shipping_address: TextView? = null
        var shipping_date: TextView? = null
    }

}