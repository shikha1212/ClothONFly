import sqlite3

# class Database():
#     dbname = "ClothONFly.db"

    # @staticmethod
    # def initialize():
    #
    #     return connect
    #
    #
    # connect = Database.initialize()

connect = sqlite3.connect("ClothONFly.db")
db = connect.cursor()
db.execute('''
              CREATE TABLE Users(User_ID INTEGER PRIMARY KEY AutoIncrement, User_Name Text NOT NULL UNIQUE, Password Text,
              User_Type Text Not Null check(User_Type = "Admin" or User_Type = "Buyer" or User_Type = "Seller"), First_Name TEXT NOT NULL,
              Last_Name TEXT NOT NULL, Email TEXT Not NUll, Address Text Not NUll, Phone_Num INTEGER Not Null)
            ''')

db.execute('''
              CREATE TABLE Inventory_Items(Item_ID INTEGER PRIMARY KEY AutoIncrement, Brand_Name TEXT NOT NULL,
              Cloth_Type TEXT NOT NULL, Size TEXT NOT NULL, Gender TEXT NOT NULL, Original_Price REAL NOT NULL,
              Rental_Price REAL NOT NULL, Available_From DATE, Owner_ID INTEGER, Location TEXT NOT NULL, Cloth_Image BLOB NOT NULL,
              Foreign Key(Owner_ID) References Users(User_ID))
            ''')

db.execute('''
              CREATE TABLE Orders (Order_ID INTEGER PRIMARY KEY AutoIncrement, User_ID INTEGER NOT NULL, Item_ID INTEGER Not Null,
              Delivery_Date Date Not Null, Return_Date Date Not Null, Shipping_Address Text Not Null,
              Order_Status Text Not Null check(Order_Status = "Order Received(Shipment Pending)" or Order_Status = "Order Shipped" or Order_Status = "Return Initiated" or Order_Status = "Return Received(Deposit Refunded)" or Order_Status = "Return Not Received(Deposit Withheld)"),
              Shipping_Date Date, FOREIGN KEY(User_ID) REFERENCES Users(User_ID), FOREIGN KEY(Item_ID) References Inventory_Item(Item_ID))
          ''')

# db.execute('''drop table Users''')
# db.execute('''drop table Inventory_Items''')
# db.execute('''drop table Orders''')

# connect.commit()







