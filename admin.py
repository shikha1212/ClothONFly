'''
Role Admin for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''
import Database

class Admin:

    def register(self,User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num):
        '''
        Description goes here
        '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        if User_Type in ('Admin','Seller'):
            print("This is an {} type user".format(User_Type))
            admin_response = input("Enter Y to add the user:")
            if admin_response.lower().startswith('y'):
                cursor.execute('''Insert into Users(User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num) values(?,?,?,?,?,?,?,?)''',
                           (User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num))
                db.commit()
            else:
                None
        else:
            cursor.execute('''Insert into Users(User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num) values(?,?,?,?,?,?,?,?)''',
                       (User_Name, Password, User_Type, First_Name, Last_Name, Email, Address, Phone_Num))
            db.commit()
        Database.Database.close_connection()

    def bulk_register(self):
        return None

    def login(self,User_Name,Password):
        '''
        Description goes here
        '''
        connect = Database.Database.initialize()
        cursor = connect.cursor()
        cur = cursor.execute('''SELECT * FROM Users where User_Name = ? AND Password = ? ''',(str(User_Name),str(Password)))
        if len(cur.fetchall()) != 0:
            print("Authentication Successful")
            return True
        else:
            print("Authentication Failed")
            return False


admin1 = Admin()
# admin1.register('1234D',123,'Buyer','Shikha','Singh','shikha@xyz.com','Lakeline,Cedar Park','123456789')
admin1.login('1234D',123)