# Role Seller for APAD Project 1

# Author: Tianyi (Kelly) Zhang
#         Shikha Singh

# Creation Date: 07/21/2019

# Major: MSITM


from ClothONFly import Database
from datetime import date
import csv
import glob


class Seller:
    image_dir = "Images/"
    export_dir = "Exports/"
    import_dir = "ImportFiles/"

    @staticmethod
    def add_item(Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From=date.today()) :
#
#         Description goes here

#
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
#         '''
#         Description goes here
#         '''
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Delete from Inventory_Items where Item_ID == ?''',(str(Item_ID)))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def update_item(Item_ID,Brand_Name,Type,Size,Gender,Original_Price,Rental_Price,Owner_ID,Location,Cloth_Image,Deposit,Available_From):
#         '''
#         Description goes here
#         '''
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
                    where Order_ID = ? and Return_Date >= ? and Order_Status = "Return Initiated" ''', (str(Order_ID),date.today()))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def withhold_deposit(Order_ID):
        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''Update Orders 
                        set Order_Status = 'Return Not Received(Deposit Withheld)'
                        where Order_ID = ? and Return_Date < ? and Order_Status != "Return Initiated" ''', (str(Order_ID),date.today()))
        db.commit()
        Database.Database.close_connection()

    @staticmethod
    def process_bulk_refunds():
        return None

    @staticmethod
    def bulk_item_upload(filename):
        for files in glob.glob(Seller.import_dir + '/*'):
            if (str(files).replace(Seller.import_dir, '')) == filename:
                with open(Seller.import_dir + '/'+filename, 'r') as inputfile:
                    items = csv.DictReader(inputfile)

                    for item in items:
                        if item['AvailableFrom'] == '':
                            item['AvailableFrom'] = date.today()
                        Seller().add_item(item['Brand'],item['Type'],item['Size'],item['Gender'],item['OriginalPrice'],item['RentalPrice'],item['OwnerID'],item['Location'],item['ClothImage'],item['Deposit'],item['AvailableFrom'])

    @staticmethod
    def all_orders():

        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''select o.Order_ID,o.Order_Status As "Order Status", o.Delivery_Date As "Delivery Date",o.Return_Date As "Return Date",o.Shipping_Address AS "Shipping Address",
                                    u.First_Name AS "Buyer's First Name",u.Last_Name AS "Buyer's LastName",u.Email AS "Buyer's Email",u.Phone_Num AS "Buyer's Contact",
                                    i.Brand_Name AS "Product's Brand",i.Type AS "Product Type", i.Size AS "Product Size",i.Gender AS "Gender",
                                    usr.First_Name as "Seller's first Name", usr.Last_Name as "Seller's Last Name", usr.Email As "Seller's Email",usr.Phone_Num AS "Seller's Contact"
                                    from Orders o join Users u on u.User_ID=o.User_ID join Inventory_Items i on o.Item_ID = i.Item_ID join Users usr on i.Owner_ID =usr.User_ID ''')


        with open(Seller.export_dir + '/' + "Orders_export_" + str(date.today()) + ".csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def orders_per_seller(Seller_ID):

        db = Database.Database.initialize()
        cursor = db.cursor()
        cursor.execute('''select User_Name from Users where User_ID = ?''',(Seller_ID,))
        for row in cursor.fetchall():
            seller = row[0]
        print(seller)
        cursor.execute('''select o.Order_ID,o.Order_Status As "Order Status", o.Delivery_Date As "Delivery Date",o.Return_Date As "Return Date",o.Shipping_Address AS "Shipping Address",
                                        u.First_Name AS "Buyer's First Name",u.Last_Name AS "Buyer's LastName",u.Email AS "Buyer's Email",u.Phone_Num AS "Buyer's Contact",
                                        i.Brand_Name AS "Product's Brand",i.Type AS "Product Type", i.Size AS "Product Size",i.Gender AS "Gender",
                                        usr.First_Name as "Seller's first Name", usr.Last_Name as "Seller's Last Name", usr.Email As "Seller's Email",usr.Phone_Num AS "Seller's Contact"
                                        from Orders o join Users u on u.User_ID=o.User_ID join Inventory_Items i on o.Item_ID = i.Item_ID join Users usr on i.Owner_ID =usr.User_ID 
                                        where usr.User_ID = ? ''', (Seller_ID,))



        with open(Seller.export_dir + '/' + seller + "'s_Orders_export_" + str(date.today()) + ".csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)


# Seller.all_orders()
Seller.orders_per_seller(2)
