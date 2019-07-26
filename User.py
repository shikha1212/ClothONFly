from ClothONFly import Database


class User():
    def __init__(self,User_Name, Password, User_Type=None, First_Name=None, Last_Name=None, Email=None, Address= None, Phone_Num=None):
        self.User_Name = User_Name
        self.Password = Password
        self.User_Type = User_Type
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.Email = Email
        self.Address = Address
        self.Phone_Num = Phone_Num


    def get_id_by_username(self):
        db = Database.Database.initialize()
        cursor = db.cursor()

        id = cursor.execute('''Select User_ID from Users where User_Name = ?''', 'Shikha123')
        if id is not None:
            return id

user1 = User('Shikha123','123')
print(user1.get_id_by_username())
