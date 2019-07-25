'''
Role Admin for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''

from random import randint
import Database
import utils

class Admin:

    def __init__(self, user_name, password, first_name, last_name, email, address, phone_num, id_num):
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone_num = phone_num
        self.id_num = id_num


    # def register(self, User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num):
    #     self.User_Name = User_Name
    #     self.Password = Password
    #     self.User_Type = User_Type
    #     self.First_Name = First_Name
    #     self.Last_Name = Last_Name
    #     self.Email = Email
    #     self.Address = Address
    #     self.Phone_Num =Phone_Num
    #     self.User_ID = randint(1000, 9999)
    #
    #     print(User_ID)

    # def register(User_Name, Password, User_Type, First_Name, Last_Name, Email, Address, Phone_Num, User_ID=None):
    #     User_ID = ra
    #     connect = Database.Database.initialize()
    #     db = connect.cursor()
    #
    #     db.execute('''Insert into Users(User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num) values(?,?,?,?,?,?,?,?)''',(User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num))
    #     connect.commit()

# admin1 = Admin()
# admin1.register(User_Name='Shikha234',Password='123',User_Type='Admin',First_Name='Shikha',Last_Name='Singh',Email='shikha@xyz.com',Address='123,streeta,123',Phone_Num='1234567890')

    #     print("Validating renter: " + renter_id_num)
    #     return False
    #
    #
    # # Check if the provided id existing seller table
    # def validate_seller(self, seller_id_num) -> bool:
    #     print("Validating seller: " + seller_id_num)
    #     return False
    #
    #
    # # Remove a specific item from the inventory table
    # def remove_item(self, item_id_num) -> bool:
    #     print("Removing item (item_id_num:  " + item_id_num + ")")
    #     return False
    #
    #
    # # Add a specific item from the inventory table
    # def add_item(self, item_id_num) -> bool:
    #     print("Adding item (item_id_num:  " + item_id_num + ")")
    #     return False
    #
    #
    # # Edit a specific item from the inventory table
    # def edit_item(self, item_id_num) -> bool:
    #     print("Adding item (item_id_num:  " + item_id_num + ")")
    #     return False
    #
    #
    # # Remove a renter from the renter table
    # def remove_renter(self, renter_id_num) -> bool:
    #     print("Removing renter (renter_id_num:  " + renter_id_num + ")")
    #     return False
    #
    #
    # # Add a renter from the renter table
    # def add_renter(self, renter_id_num) -> bool:
    #     print("Adding renter (renter_id_num:  " + renter_id_num + ")")
    #     return False
    #
    #
    # # Remove a seller from the seller table
    # def remove_seller(self, seller_id_num) -> bool:
    #     print("Removing seller (seller_id_num:  " + seller_id_num + ")")
    #     return False
    #
    #
    # # Add a seller from the seller table
    # def add_seller(self, seller_id_num) -> bool:
    #     print("Adding seller (seller_id_num:  " + seller_id_num + ")")
    #     return False
