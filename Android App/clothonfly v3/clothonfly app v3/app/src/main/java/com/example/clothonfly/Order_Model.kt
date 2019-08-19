package com.example.clothonfly

class Order_Model {

    var order_id: String? = null
    var order_status: String? = null
    var item_id: String? = null
    var delivery_date: String? = null
    var return_date: String? = null
    var actual_return_date: String? = null
    var shipping_address: String? = null
    var shipping_date: String? = null

    fun getOrderId(): String {
        return order_id.toString()
    }

    fun getOrderStatus(): String {
        return order_status.toString()
    }

    fun getItemId(): String {
        return item_id.toString()
    }

    fun getDeliveryDate(): String {
        return delivery_date.toString()
    }

    fun getReturnDate(): String {
        return return_date.toString()
    }

    fun getActualReturnDate(): String {
        return actual_return_date.toString()
    }

    fun getShippingAddress(): String {
        return shipping_address.toString()
    }

    fun getShippingDate(): String {
        return shipping_date.toString()
    }

    fun setOrderId(order_id: String) {
        this.order_id = order_id
    }

    fun setOrderStatus(order_status: String) {
        this.order_status = order_status
    }

    fun setItemId(item_id: String) {
        this.item_id = item_id
    }

    fun setDeliveryDate(delivery_date: String) {
        this.delivery_date = delivery_date
    }

    fun setReturnDate(return_date: String) {
        this.return_date = return_date
    }

    fun setActualReturnDate(actual_return_date: String) {
        this.actual_return_date = actual_return_date
    }

    fun setShippingAddress(shipping_address: String){
        this.shipping_address = shipping_address
    }

    fun setShippingDate(shipping_date: String) {
        this.shipping_date = shipping_date
    }
}