package com.example.clothonfly


import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import com.android.volley.toolbox.NetworkImageView
import com.bumptech.glide.Glide
import kotlinx.android.synthetic.main.buyer_home.view.*
import kotlinx.android.synthetic.main.clothing_items.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONObject

//import com.squareup.picasso.Picasso


/**
 * Orignial author: Parsania Hardik on 03-Jan-17.
 * Modified by Ramesh Yerraballi on 8/12/19
 */
class CustomAdapter(private val context: Context, private val itemsModelArrayList: ArrayList<Item_Model>) :
    BaseAdapter() {

    override fun getViewTypeCount(): Int {
        return count
    }

    override fun getItemViewType(position: Int): Int {

        return position
    }

    override fun getCount(): Int {
        return itemsModelArrayList.size
    }

    override fun getItem(position: Int): Any {
        return itemsModelArrayList[position]
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
            convertView = inflater.inflate(R.layout.clothing_items, null, true)

            holder.item_id = convertView!!.findViewById(R.id.item_id) as TextView
            holder.rental_price = convertView.findViewById(R.id.rental_price) as TextView
            holder.original_price = convertView!!.findViewById(R.id.original_price) as TextView
            holder.deposit = convertView!!.findViewById(R.id.deposit) as TextView
            holder.brand = convertView!!.findViewById(R.id.brand) as TextView
            holder.size = convertView!!.findViewById(R.id.size) as TextView
            holder.imageView2 = convertView.findViewById(R.id.imageView2) as ImageView



//            convertView.tag = holder
//
//            convertView.rent_button.setOnClickListener {
//                doAsync {
//                    var response = rent_item(itemsModelArrayList[position].getID(),orderModelArrayList[position].getItemId())
//                    val json = JSONObject(response)
//                    if (json.get("message") == "Succeeded") {
//                        // TODO
//                    } else {
//                        println("Sign up failed!!!")
//                        Log.d("Refresh failed", "Failed to refresh the scroll listing view\n")
//                    }
//                }
//            }


            convertView.select_item.setOnClickListener({
                            // Set global item id
                Global.setitemid(itemsModelArrayList[position].getID())
                Global.setimg(itemsModelArrayList[position].getimage())
        })

        } else {
            // the getTag returns the viewHolder object set as a tag to the view
            holder = convertView.tag as ViewHolder
        }

        holder.item_id!!.text = "Item ID: " + itemsModelArrayList[position].getID()
        holder.rental_price!!.text = "Rental Price: " + itemsModelArrayList[position].getRentalPrice() + " $"
        holder.original_price!!.text = "Original Price: " + itemsModelArrayList[position].getOriginalPrice() + " $"
        holder.deposit!!.text = "Deposit: " +itemsModelArrayList[position].getdeposit() + " $"
        holder.brand!!.text = "Brand: " +itemsModelArrayList[position].getbrand()
        holder.size!!.text = "Size: " +itemsModelArrayList[position].getsize()
//        val url =  "https://cloth-on-fly.appspot.com/look/27.png"
//        Picasso.with(context)
//            .load(url)
//            .into(holder.imageView2);


        Glide.with(context).load("https://cloth-on-fly.appspot.com/look/" +itemsModelArrayList[position].getimage()).into(holder.imageView2)

        return convertView
    }

    private inner class ViewHolder {

        var imageView2: ImageView? = null
        var item_id: TextView? = null
        var rental_price: TextView? = null
        var original_price: TextView? = null
        var brand: TextView? = null
        var size: TextView? = null
        var deposit: TextView? = null
    }

}