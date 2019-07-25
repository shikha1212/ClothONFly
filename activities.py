'''
The activity APIs for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''

import utils
from admin import Admin
from seller import Seller
from buyer import Buyer
import Database


def register(user_role) -> bool:
    user_name = utils.TEST_ADMIN_NAME
    password = utils.TEST_PASSWORD
    first_name = utils.TEST_FIRST_NAME
    last_name = utils.TEST_LAST_NAME
    email = utils.TEST_EMAIL
    address = utils.TEST_ADDRESS
    phone_num = utils.TEST_PHONE_NUM
    id_num = utils.TEST_ID_NUM

    if user_role == utils.ADMIN_ROLE_NAME:
        new_admin_user = Admin(user_name, password, first_name,
                               last_name, email, address, phone_num, id_num)
        write_user_into_database(user_role, new_admin_user)
    elif user_role == utils.SELLER_ROLE_NAME:
        new_seller_user = Seller(user_name, password, first_name,
                               last_name, email, address, phone_num, id_num)
        write_user_into_database(user_role, new_seller_user)
    elif user_role == utils.BUYER_ROLE_NAME:
        new_buyer_user = Buyer(user_name, password, first_name,
                                 last_name, email, address, phone_num, id_num)
        write_user_into_database(user_role, new_buyer_user)
    else:
        print("Unknown role")
        return False

    return True


def write_user_into_database(user_role, user):
    connect = Database.Database.initialize()
    db = connect.cursor()

    db.execute(
        '''Insert into Users(User_Name, Password, User_Type, First_Name, Last_Name, Email, Address, Phone_Num, User_ID) values(?,?,?,?,?,?,?,?,?)''',
        (user.user_name, user.password, user_role, user.first_name, user.last_name, user.email, user.address, user.phone_num, user.id_num))
    connect.commit()
