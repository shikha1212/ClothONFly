package com.example.clothonfly

object Global {

    private var user_name: String? = null
    private var total_price: String? = null
    private var item_id: String? = null
    private var days: String? = null
    private var img: String?= null

    fun setUserName(user_name: String) {
        this.user_name = user_name
    }

    fun getUserName(): String? {
        return this.user_name
    }

    fun setprice(total_price: String) {
        this.total_price = total_price
    }

    fun getprice(): String? {
        return this.total_price
    }


    fun setitemid(item_id: String) {
        this.item_id = item_id
    }

    fun get_itemid(): String? {
        return this.item_id
    }

    fun setdays(days: String) {
        this.days = days
    }

    fun getdays(): String? {
        return this.days
    }


    fun setimg(img: String) {
        this.img = img
    }

    fun getimg(): String? {
        return this.img
    }


}