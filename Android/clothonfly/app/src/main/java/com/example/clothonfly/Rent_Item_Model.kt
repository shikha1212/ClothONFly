package com.example.clothonfly

class Rent_Item_Model {

    var user_name: String? = null
    var item_id: String? = null
    var rental_price: String? = null
    var rent_days: String? = null
    var shipping_address: String? = null

    fun getUserName(): String {
        return user_name.toString()
    }

    fun setUserName(user_name: String) {
        this.user_name = user_name
    }

    fun getItemID(): String {
        return item_id.toString()
    }

    fun setItemID(name: String) {
        this.item_id = name
    }

    fun getRentalPrice(): String {
        return rental_price.toString()
    }

    fun setRentalPrice(name: String) {
        this.rental_price = name
    }

    fun getRentDays(): String {
        return rent_days.toString()
    }

    fun setRentDays(rent_days: String) {
        this.rent_days = rent_days
    }

    fun getShippingAddress(): String {
        return shipping_address.toString()
    }

    fun setShippingAddress(shipping_address: String) {
        this.shipping_address = shipping_address
    }

}
