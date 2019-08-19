package com.example.clothonfly

class Item_Model {

    var item_id: String? = null
    var rental_price: String? = null

    fun getID(): String {
        return item_id.toString()
    }

    fun setID(name: String) {
        this.item_id = name
    }

    fun getRentalPrice(): String {
        return rental_price.toString()
    }

    fun setRentalPrice(name: String) {
        this.rental_price = name
    }

}
