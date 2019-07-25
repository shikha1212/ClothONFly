'''
Role Seller for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''

class Seller:

    def __init__(self, user_name, password, first_name, last_name, email, address, phone_num, id_num):
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone_num = phone_num
        self.id_num = id_num

    def add_item(self, item_id_num) -> bool:
        print("Adding item (item_id_num:  " + item_id_num + ") to the inventory")
        return False


    def remove_item(self, item_id_num) -> bool:
        print("Removing item (item_id_num:  " + item_id_num + ")")
        return False
