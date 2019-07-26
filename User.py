import Database

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

    @classmethod
    def get_by_username(cls, User_Name):
        data = Database.find_one('users', {'email': email})
        print(data)
        if data is not None:
            return cls(**data)