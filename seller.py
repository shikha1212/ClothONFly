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
import csv
import glob

class Seller:
    image_dir = "Images/"
    export_dir ="Exports/"
    import_dir = "Import_Files/"

    @staticmethod
    def add_item(Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From=date.today()) :
        '''
        Description goes here

        '''
        db = Database.Database.initialize()
        cursor = db.cursor()

        for image in glob.glob(Seller.image_dir+'/*'):
           if (str(image).replace(Seller.image_dir,'')) == Cloth_Image:
                with open(image, 'rb') as file:
                    blobData = file.read()

        cursor.execute(
            '''Insert into Inventory_Items(Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From) values(?,?,?,?,?,?,?,?,?,?,?)''',
            (Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,blobData,Deposit,Available_From))
        db.commit()

        Database.Database.close_connection()

    @staticmethod
    def remove_item(Item_ID):
        '''
        Description goes here
        '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Delete from Inventory_Items where Item_ID == ?''',(str(Item_ID)))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def update_item(Item_ID,Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From):
        '''
        Description goes here
        '''
        db = Database.Database.initialize()
        cursor = db.cursor()

        for image in glob.glob(Seller.image_dir + '/*'):
            if (str(image).replace(Seller.image_dir, '')) == Cloth_Image:
                with open(image, 'rb') as file:
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

    @staticmethod
    def ship_item(Order_ID):
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Update Orders 
                set Order_Status = 'Order Shipped',
                    Shipping_Date = ?
                where Order_ID = ?''', (date.today(),Order_ID))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def refund_deposit(Order_ID):
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Update Orders 
                    set Order_Status = 'Return Received(Deposit Refunded)'
                    where Order_ID = ?''', (str(Order_ID)))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def withhold_deposit(Order_ID):
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Update Orders 
                        set Order_Status = 'Return Not Received(Deposit Withheld)'
                        where Order_ID = ?''', (str(Order_ID)))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def process_bulk_refunds():
        return None

    @staticmethod
    def bulk_item_upload(filename):
        for file in glob.glob(Seller.import_dir+'/*'):
            if (str(file).replace(Seller.import_dir,'')) == filename:
                with open(filename,'r') as myfile:
                    items = csv.DictReader(myfile)
                    for item in items:
                        if item['AvailableFrom'] == '':
                            item['AvailableFrom'] = date.today()
                            Seller().add_item(item['Brand'], item['Type'],item['Size'],item['Gender'],item['OriginalPrice'],item['RentalPrice'],item['OwnerID'],item['Location'],item['ClothImage'],item['Deposit'],item['AvailableFrom'])

    # @staticmethod
    # def export_all_orders():
    #
    #     db = Database.Database.initialize()
    #     cursor = db.cursor()
    #     cursor.execute('''select * from Orders join Users on Orders.User_ID=Users.User_ID join Inventory_Items on Orders.Item_ID = Inventory_Items.Item_ID''')
    #     with open("All_Orders_export.csv", "w", newline='') as file:
    #         csv_writer = csv.writer(file)
    #         csv_writer.writerow([i[0] for i in cursor.description])  # write headers
    #         csv_writer.writerows(cursor)


Seller.bulk_item_upload('ItemInventory.csv')
# seller1.remove_item(Item_ID=3)
# Seller.update_item(Item_ID=15,Brand_Name="Puma",Type="T-shirt",Size="M",Gender="Male",Original_Price=50,Rental_Price=10,Owner_ID=1,Location="Austin",Cloth_Image="shirt.jpg",Deposit=20,Available_From="2019-07-22")
#
# Seller.withhold_deposit(1)
# Seller.export_all_orders()

