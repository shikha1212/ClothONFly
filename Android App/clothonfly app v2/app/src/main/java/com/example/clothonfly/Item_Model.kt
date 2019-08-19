package com.example.clothonfly

class Item_Model {

    var item_id: String? = null
    var rental_price: String? = null
    var brand: String? = null
    var size: String? = null
    var original_price: String? = null
    var deposit: String? = null
    var image: String? = null

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

    fun getOriginalPrice(): String {
        return original_price.toString()
    }

    fun setOriginalPrice(name: String) {
        this.original_price = name
    }

    fun getdeposit(): String {
        return deposit.toString()
    }

    fun setdeposit(name: String) {
        this.deposit = name
    }


    fun getbrand(): String {
        return brand.toString()
    }

    fun setbrand(name: String) {
        this.brand = name
    }

    fun getsize(): String {
        return size.toString()
    }

    fun setsize(name: String) {
        this.size = name
    }

    fun getimage(): String {
        return image.toString()
    }

    fun setimage(image: String) {
        this.image = image
    }
}
