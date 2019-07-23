'''
Role Seller for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''
import sqlite3
import Database
from datetime import date, datetime

class Seller:

    def add_item(self,Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From=date.today()) :
        '''
        Description goes here

        '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        with open(Cloth_Image, 'rb') as file:
            blobData = file.read()
        cursor.execute(
            '''Insert into Inventory_Items(Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From) values(?,?,?,?,?,?,?,?,?,?,?)''',
            (Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,blobData,Deposit,Available_From))
        db.commit()

        Database.Database.close_connection()

    def remove_item(self,Item_ID):
        '''
        Description goes here
        '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Delete from Inventory_Items where Item_ID == ?''',(str(Item_ID)))
        db.commit()
        Database.Database.close_connection()


    def update_item(self,Item_ID,Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From):
        '''
        Description goes here
        '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        with open(Cloth_Image, 'rb') as file:
            blobData = file.read()
        cursor.execute('''Update Inventory_Items 
        set Brand_Name= ?,
        Type = ? ,
        Size =?,
        Gender = ?,
        Original_Price =?,
        Rental_Price =?,
        Owner_ID=?,
        Location=?,
        Cloth_Image=?,
        Deposit=?,
        Available_From=? where Item_ID = ?''',(Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,blobData,Deposit,Available_From,Item_ID))
        db.commit()
        Database.Database.close_connection()


    def ship_item(self,):

seller1 = Seller()
seller1.remove_item(Item_ID=3)
seller1.add_item(Brand_Name="Nike",Type="T-shirt",Size="M",Gender="Male",Original_Price=50,Rental_Price=10,Owner_ID=1,Location="Austin",Cloth_Image="shirt.jpg",Deposit=20,Available_From="2019-07-22")



