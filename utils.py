'''
The utility functions for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''


from uuid import uuid4

ADMIN_ROLE_NAME = 'Admin'
BUYER_ROLE_NAME = 'Renter'
SELLER_ROLE_NAME = "Seller"

TEST_ADMIN_NAME = 'KellyZhang'
TEST_PASSWORD = '123'
TEST_FIRST_NAME = 'Kelly'
TEST_LAST_NAME = 'Zhang'
TEST_EMAIL = '123abc@def.com'
TEST_ADDRESS = '123 FASDF, AUSTIN, TX 78731'
TEST_PHONE_NUM = '123-456-7890'
TEST_ID_NUM = '70e52cb3-47b5-4aa5-a0cd-827766845385'


def generate_id_for_role() -> str:
    print("Generating UUID for role!!!!!")
    return str(uuid4())

