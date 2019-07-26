from admin import Admin
import seller


User_Name = input("Enter your user name:")
Password = input("Enter your user name:")
User_Type = input("Enter your user name:")
First_Name = input("Enter your user name:")
Last_Name = input("Enter your user name:")
Email = input("Enter your user name:")
Address = input("Enter your user name:")
Phone_Num = input("Enter your user name:")

# Admin.register(User_Name,Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num)
Admin.login(User_Name,Password)
