package com.example.clothonfly


import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import java.util.ArrayList

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

            convertView.tag = holder
        } else {
            // the getTag returns the viewHolder object set as a tag to the view
            holder = convertView.tag as ViewHolder
        }

        holder.item_id!!.text = "Item ID: " + itemsModelArrayList[position].getID()
        holder.rental_price!!.text = "Rental Price: " + itemsModelArrayList[position].getRentalPrice()

        return convertView
    }

    private inner class ViewHolder {

        var item_id: TextView? = null
        var rental_price: TextView? = null
    }

}