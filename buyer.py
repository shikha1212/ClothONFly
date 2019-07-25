'''
Role Buyer for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''


class Buyer:

    def __init__(self, user_name, password, first_name, last_name, email, address, phone_num, id_num):
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone_num = phone_num
        self.id_num = id_num
        self.shopping_cart = []

    def add_item_to_shopping_cart(self, item_id_num) -> bool:
        print("Adding item (item_id_num:  " + item_id_num + ") to shopping cart")
        self.shopping_cart.append(item_id_num)
        return True

    def remove_item_to_shopping_cart(self, item_id_num) -> bool:
        print("Removing item (item_id_num:  " + item_id_num + ") to shopping cart")
        self.shopping_cart.remove(item_id_num)
        return True

    def rent_item(self) -> bool:
        print("Renting item from the shopping cart")
        for item in self.shopping_cart:
            # add item into Orders table
            # remove item from Inventory_Items table
            return False

    def return_item(self, item_id_num) -> bool:
        print("Returning item (item_id_num:  " + item_id_num + ")")
        # add item into Inventory_Items table
        # remove item from Orders table
        return False
