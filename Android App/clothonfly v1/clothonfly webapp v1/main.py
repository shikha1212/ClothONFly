# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_mysql]
# add1
import os
from flask import Flask, jsonify, session, redirect, url_for, escape, render_template, request, send_file, Response,send_from_directory,logging
from google.cloud import storage
from google.cloud.storage import Blob
from werkzeug.utils import secure_filename
import io
from datetime import date, datetime, timedelta

import pymysql
# import base64
# add2
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__, template_folder='template')
app.config['secret_key'] = 'secret123456'

def db_connect():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        return pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name,cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        return pymysql.connect(user=db_user, password=db_password,
                               host=host, db=db_name, cursorclass=pymysql.cursors.DictCursor)



# def convertToBinaryData(filename):
#     #Convert digital data to binary format
#
#     with open("filename", "rb") as imageFile:
#         binaryData = base64.b64encode(imageFile.read())
#         return binaryData

@app.route("/")
def home(message=''):
    message=message
    return render_template('login.html',message=message)

@app.route("/login", methods = ['POST', 'GET'])
def check_action():
    if request.form['action'] == "Log In":
        conn = db_connect()
        user_name = request.form['user_name']
        Password = request.form['password']

        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Users where User_Name = %s AND Password = %s', (user_name, Password))
            result = cursor.fetchall()
            if len(result) == 1:
                for row in result:
                    role = row['User_Type']
                    conn.close()

                    if role == 'Buyer':
                        return buyer_home(user_name)

                    elif role == 'Seller':
                        return seller_home(user_name)
                    elif role == 'Admin':
                        return admin_home(user_name)
            else:
                return render_template("login.html",message="Incorrect username/password")

    elif request.form['action'] == "Sign Up":
        return render_template('register.html')

@app.route("/buyerhome/<string:user_name>", methods = ['POST', 'GET'])
def buyer_home(user_name):
    user_name = user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Inventory_Items where Available_From <= %s', date.today())
        items = cursor.fetchall()
    conn.close()
    return render_template("buyerhome.html", items=items, user_name=user_name)


@app.route("/sellerhome/<string:user_name>", methods = ['POST', 'GET'])
def seller_home(user_name, message =''):
    message = message
    user_name = user_name
    return render_template("sellerhome.html", user_name=user_name, message = message)

@app.route("/register/success", methods=['POST'])
def add_user():
    conn = db_connect()
    User_Name = request.form['user_name']
    Password = request.form['password']
    User_Type = request.form['user_type']
    First_Name = request.form['first_name']
    Last_Name = request.form['last_name']
    Email = request.form['email']
    Address = request.form['address']
    Phone_Num = request.form['contact']

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Users where User_Name = %s', User_Name)
        result = cursor.fetchall()
        if len(result) > 0:
            return render_template('register.html', message="Registration Failed !! This User Name is already in use. Please use a different User Name")

    with conn.cursor() as cursor:
        cursor.execute('Insert into Users(User_Name, Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num) values(%s,%s,%s,%s,%s,%s,%s,%s)',
                        (User_Name, Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num))
        conn.commit()
        conn.close()

    return render_template('login.html',message = "Registration successful !! Please login to continue")



@app.route("/uploader/<string:user_name>", methods = ['POST','GET'])
def upload(user_name):

    Brand_Name = request.form['brand']
    Cloth_Type = request.form['type']
    Size = request.form['size']
    Gender = request.form['gender']
    Original_Price = request.form['original_price']
    Rental_Price = request.form['rental_price']
    Location = request.form['location']
    Deposit = request.form['deposit']
    Available_From = date.today()

    if request.method == 'POST':
        file = request.files['file']

    file_name = str(file.filename)
    bucket_name = 'clothonfly_bucket'
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(secure_filename(file.filename))
    try:
        blob.upload_from_file(file.stream)
        conn = db_connect()

        with conn.cursor() as cursor:
            cursor.execute('SELECT * from Users where User_Name = %s', (user_name))
            users = cursor.fetchall()
            for user in users:
                Owner_ID = user['User_ID']

        with conn.cursor() as cursor:
            cursor.execute(
                'Insert into Inventory_Items(Brand_Name, Cloth_Type, Size, Gender, Original_Price, Rental_Price, Owner_ID, Location, Cloth_Image, Deposit, Available_From) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (Brand_Name, Cloth_Type, Size, Gender, Original_Price, Rental_Price, Owner_ID, Location, file_name,
                 Deposit, Available_From))
        conn.commit()
        conn.close()
        return seller_home(user_name,
                           message="The item is added in inventory and will be available for renting from today.")


    except Exception as e:
        logging.exception(e)
        return jsonify({"success": False})




@app.route("/rent/item/<string:Item_ID>/<string:user_name>", methods = ['POST', 'GET'])
def input_days_of_rent(Item_ID,user_name):
    user_name = user_name
    Item_ID = Item_ID
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Inventory_Items where Item_ID=%s',Item_ID)
        items = cursor.fetchall()
    conn.close()
    return render_template("inputdaysofrent.html",items = items,user_name = user_name)


@app.route('/calculate_price/<string:Item_ID>/<string:user_name>',methods = ['POST','GET'])
def calculate_price(Item_ID,user_name):
    user_name = user_name
    Item_ID = Item_ID
    days = float(request.form['days'])

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Inventory_Items where Item_ID= %s',Item_ID)
        items = cursor.fetchall()
        for item in items:
            rental_price = float(item['Rental_Price'])
            deposit = float(item['Deposit'])

    total_price = deposit + (days * rental_price)
    conn.close()
    return render_template("confirmorder.html",total_price=total_price,days=days,items=items,user_name = user_name)

@app.route('/confirm_order/<string:Item_ID>/<string:user_name>/<float:days>',methods = ['POST','GET'])
def confirm_order(Item_ID,user_name,days):
    user_name = user_name
    shipping_address = request.form['address']
    delivery_date = date.today() + timedelta(days=7)
    days = int(days)
    return_date = delivery_date + timedelta(days=days)
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Users where user_name = %s',user_name)
        items = cursor.fetchall()
        for item in items:
            User_ID = item['User_ID']
            conn.close()

    Item_ID = Item_ID

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Orders(User_ID, Item_ID, Delivery_Date, Return_Date, Shipping_Address, Order_Status) VALUES(%s,%s,%s,%s,%s,%s)',
                        (User_ID,Item_ID,delivery_date,return_date,shipping_address,"Order Received(Shipment Pending)"))
        conn.commit()
        conn.close()

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Update Inventory_Items set Available_From = NULL where Item_ID=%s ',Item_ID)
        conn.commit()
        conn.close()

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Orders where User_Id = %s AND Item_ID = %s',(User_ID,Item_ID))
        orders = cursor.fetchall()
        for order in orders:
            orderid = order['Order_ID']

        conn.close()

    return my_orders(user_name=user_name,message="Order Confirmed !! Order ID: " + str(orderid))


@app.route('/Myorders/<string:user_name>',methods = ['POST','GET'])
def my_orders(user_name,message='',message1=''):
    user_name = user_name
    message=message
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s',user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Orders where User_ID = %s', user_id)
        orders = cursor.fetchall()
        if len(orders) == 0:
            message = "You don't have any orders yet"
        else:
            message = "Here are your orders"
        conn.close()
    return render_template('myorders.html',orders=orders,user_name=user_name,message=message,message1=message1)

@app.route('/return_item/<string:Order_ID>/<string:Item_ID>/<string:user_name>',methods = ['POST','GET'])
def return_item(Order_ID,Item_ID,user_name):
    Order_ID = Order_ID
    Item_ID = Item_ID
    user_name = user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Orders where Order_ID = %s',Order_ID)
        orders = cursor.fetchall()
        conn.close()
        for order in orders:
            orderstatus = order['Order_Status']

        if orderstatus == "Order Shipped":
            conn = db_connect()
            with conn.cursor() as cursor:
                cursor.execute('Update Orders set Order_Status = "Order Returned",Actual_Return_Date=%s where Order_ID = %s',(date.today(),Order_ID))
                conn.commit()
                conn.close()
                conn = db_connect()
                with conn.cursor() as cursor:
                    cursor.execute('Update Inventory_Items set Available_From = %s where Item_ID = %s',(date.today(),Item_ID))
                    conn.commit()
                    conn.close()
            return my_orders(user_name,message1 =" -- Item has been returned to seller")
        else:
            return my_orders(user_name,message1 =" -- This item is not eligible for return")


@app.route('/all_orders_for_seller/<string:user_name>',methods = ['POST','GET'])
def all_orders_for_seller(user_name):
    user_name =user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s', user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('''Select o.Order_ID 'Order_ID', o.Item_ID 'Item_ID', o.Delivery_Date 'Delivery_Date', o.Return_Date 'Return_Date',
                        o.Shipping_Address 'Shipping_Address',o.Order_Status 'Order_Status',o.Shipping_Date 'Shipping_Date',
                        u.First_Name 'Buyer_FN', u.Last_Name 'Buyer_LN',u.Email 'Buyer_email',u.Phone_Num 'Buyer_Contact',
                        i.Brand_Name 'Brand', i.Cloth_Type 'Type', i.Size 'Size', i.Gender 'Gender',
                        i.Original_Price 'Original_Price',i.Rental_Price 'Rental_Price',i.Deposit 'Deposit'
                        FROM Orders o JOIN Users u ON u.User_ID = o.User_ID JOIN Inventory_Items i on i.Item_ID = o.Item_ID where i.Owner_ID = %s''', (user_id))

        orders = cursor.fetchall()
        if len(orders) == 0:
            message = "You currently don't have any orders."
        else:
            message = "Here are all your orders"
        conn.close()
        return render_template("allordersforseller.html",user_name=user_name,orders=orders,message=message)


@app.route('/orders_for_shipment/<string:user_name>',methods = ['POST','GET'])
def orders_for_shipment(user_name,message=''):
    user_name = user_name
    message = message
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s', user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('''Select o.Order_ID 'Order_ID', o.Item_ID 'Item_ID', o.Delivery_Date 'Delivery_Date', o.Return_Date 'Return_Date',
                            o.Shipping_Address 'Shipping_Address',o.Order_Status 'Order_Status',o.Shipping_Date 'Shipping_Date',
                            u.First_Name 'Buyer_FN', u.Last_Name 'Buyer_LN',u.Email 'Buyer_email',u.Phone_Num 'Buyer_Contact',
                            i.Brand_Name 'Brand', i.Cloth_Type 'Type', i.Size 'Size', i.Gender 'Gender',
                            i.Original_Price 'Original_Price',i.Rental_Price 'Rental_Price',i.Deposit 'Deposit'
                            FROM Orders o JOIN Users u ON u.User_ID = o.User_ID JOIN Inventory_Items i on i.Item_ID = o.Item_ID where o.Order_Status='Order Received(Shipment Pending)' AND i.Owner_ID = %s''',
                       (user_id))

        orders = cursor.fetchall()
        if len(orders) == 0:
            message = "You currently don't have any orders for shipment."
        else:
            message = "Here are your orders ready for shipment"
        conn.close()
        return render_template("orders_for_shipment.html",message=message, user_name=user_name, orders=orders)

@app.route('/ship_item/<string:Order_ID>/<string:Item_ID>/<string:user_name>',methods = ['POST','GET'])
def ship_item(Order_ID,Item_ID,user_name):
    Order_ID = Order_ID
    Item_ID = Item_ID
    user_name = user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Update Orders set Order_Status="Order Shipped", Shipping_date = %s where Order_ID = %s', (date.today(),Order_ID))
        conn.commit()
        conn.close()
        return orders_for_shipment(user_name, message="Item :" + Item_ID + "has been shipped to seller")


@app.route('/orders_for_depositrefund/<string:user_name>',methods = ['POST','GET'])
def orders_for_depositrefund(user_name,message=''):
    user_name = user_name
    message = message
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s', user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('''Select o.Order_ID 'Order_ID', o.Item_ID 'Item_ID', o.Delivery_Date 'Delivery_Date', o.Return_Date 'Return_Date',
                                o.Shipping_Address 'Shipping_Address',o.Order_Status 'Order_Status',o.Shipping_Date 'Shipping_Date',
                                u.First_Name 'Buyer_FN', u.Last_Name 'Buyer_LN',u.Email 'Buyer_email',u.Phone_Num 'Buyer_Contact',
                                i.Brand_Name 'Brand', i.Cloth_Type 'Type', i.Size 'Size', i.Gender 'Gender',
                                i.Original_Price 'Original_Price',i.Rental_Price 'Rental_Price',i.Deposit 'Deposit'
                                FROM Orders o JOIN Users u ON u.User_ID = o.User_ID JOIN Inventory_Items i on i.Item_ID = o.Item_ID where o.Order_Status='Order Returned' AND i.Owner_ID = %s AND o.Actual_Return_Date<= o.Return_Date''',
                       (user_id))

        orders = cursor.fetchall()
        if len(orders) == 0:
            message = "You currently don't have any orders for deposit refund."
        else:
            message = "Here are your orders for a deposit refund"
        conn.close()
        return render_template("orders_for_depositrefund.html", message=message, user_name=user_name, orders=orders)

@app.route('/refund_deposit/<string:Order_ID>/<string:Item_ID>/<string:user_name>',methods = ['POST','GET'])
def refund_deposit(Order_ID,Item_ID,user_name):
    Order_ID = Order_ID
    Item_ID = Item_ID
    user_name = user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Update Orders set Order_Status="Return Received(Deposit Refunded)" where Order_ID = %s', Order_ID)
        conn.commit()
        conn.close()
        return orders_for_depositrefund(user_name, message="Deposit for order " + Order_ID + "has been refunded back to buyer")

@app.route('/orders_for_depositwithhold/<string:user_name>',methods = ['POST','GET'])
def orders_for_depositwithhold(user_name,message=''):
    user_name = user_name
    message = message
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s', user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('''Select o.Order_ID 'Order_ID', o.Item_ID 'Item_ID', o.Delivery_Date 'Delivery_Date', o.Return_Date 'Return_Date',
                                o.Shipping_Address 'Shipping_Address',o.Order_Status 'Order_Status',o.Shipping_Date 'Shipping_Date',
                                u.First_Name 'Buyer_FN', u.Last_Name 'Buyer_LN',u.Email 'Buyer_email',u.Phone_Num 'Buyer_Contact',
                                i.Brand_Name 'Brand', i.Cloth_Type 'Type', i.Size 'Size', i.Gender 'Gender',
                                i.Original_Price 'Original_Price',i.Rental_Price 'Rental_Price',i.Deposit 'Deposit'
                                FROM Orders o JOIN Users u ON u.User_ID = o.User_ID JOIN Inventory_Items i on i.Item_ID = o.Item_ID 
                                where i.Owner_ID = %s AND o.Order_Status != 'Return Not Received(Deposit Withheld)' AND
                                (o.Actual_Return_Date > o.Return_Date OR (o.Actual_Return_Date is Null and o.Return_Date<%s)) ''',(user_id,date.today()))

        orders = cursor.fetchall()
        if len(orders) == 0:
            message = "You currently don't have any orders for withholding deposit."
        else:
            message = "Here are your orders that are not returned on time !! Click on withhold deposit if you want to withhold the deposit amount or contact buyer offline"

        conn.close()
        return render_template("orders_for_depositwithhold.html", message=message, user_name=user_name, orders=orders)


@app.route('/withhold_deposit/<string:Order_ID>/<string:Item_ID>/<string:user_name>',methods = ['POST','GET'])
def withhold_deposit(Order_ID,Item_ID,user_name):
    Order_ID = Order_ID
    Item_ID = Item_ID
    user_name = user_name
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Update Orders set Order_Status="Return Not Received(Deposit Withheld)" where Order_ID = %s', Order_ID)
        conn.commit()
        conn.close()
        return orders_for_depositrefund(user_name, message="Deposit for order " + Order_ID + "has been withheld")

@app.route('/logout')
def logout():
    response = Response()
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return home("Successfully Logged Out")


@app.route("/admin/home/<string:user_name>",methods = ['POST', 'GET'])
def admin_home(user_name,message =''):
    message = message
    user_name = user_name
    return render_template("adminhome.html",user_name=user_name,message = message)

@app.route("/adminremoveu/<string:user_name>", methods=['POST','GET'])
def adminremoveu(user_name):
    user_name = user_name
    return render_template("userremoved.html",user_name=user_name)

@app.route("/adminremovei/<string:user_name>", methods=['POST','GET'])
def adminremovei(user_name):
    user_name = user_name
    return render_template("itemremoved.html", user_name=user_name)

@app.route("/userremoved/<string:user_name>", methods=['POST','GET'])
def remove_user(user_name):
  user_name = user_name
  UserName = request.form['user_name']
  conn = db_connect()
  with conn.cursor() as cursor:
      cursor.execute('DELETE FROM Users WHERE User_Name = %s', UserName)
  conn.commit()
  conn.close()
  return admin_home(message="User removed successfully", user_name=user_name)

@app.route("/itemremoved/<string:user_name>", methods=['POST','GET'])
def remove_item(user_name):
    user_name = user_name
    Item_ID = request.form['item_id']
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * FROM Orders WHERE Item_ID = %s', Item_ID)
        orders = cursor.fetchall()
        if len(orders) > 0:
            return admin_home(message="This Item cannot be removed as it is in order history", user_name=user_name)
        else:
            cursor.execute('DELETE FROM Inventory_Items WHERE Item_ID = %s', Item_ID)
            conn.commit()
            conn.close()
            return admin_home(message="Item removed successfully", user_name=user_name)







# @app.route("/uploader/<string:user_name>", methods=["POST"])
# def uploading(user_name):
#     user_name = user_name
#
#     if request.method == 'POST':
#         file = request.files['file']
#
#     file_name = str(file.filename)
#     bucket_name = 'clothonfly_bucket'
#     client = storage.Client()
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(secure_filename(file.filename))
#     try:
#         blob.upload_from_file(file.stream)
#         return item_added(user_name = user_name, filename = file_name)
#         # return jsonify({"success": True})
#
#     except Exception as e:
#         logging.exception(e)
#         return jsonify({"success": False})


#
# @app.route("/upload_image/<string:user_name>/", methods=["POST"])
# def upload_image(user_name):
#     user_name = user_name
#
#     Password = request.form['password']
#     User_Type = request.form['user_type']
#     First_Name = request.form['first_name']
#     Last_Name = request.form['last_name']
#     Email = request.form['email']
#     Address = request.form['address']
#     Phone_Num = request.form['contact']
#
#     return render_template("upload_image.html",user_name=user_name)



@app.route('/look/<filename>')
def flook(filename):

    filename=filename
    try:
        # Reformat the filename using the bucket name fetched above
        bucket_name = 'clothonfly_bucket'
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(secure_filename(filename))
        data = blob.download_as_string()
        extension = secure_filename(filename).rsplit('.', 1)[1]
        if extension == "png":
            return send_file(io.BytesIO(data), attachment_filename=filename, mimetype='image/png')
        else:
            return data
    except Exception as e:
        return jsonify({'error': 'Could not find file {}'.format(filename)})


@app.route("/validate_user", methods = ['POST', 'GET'])
def validate_user():
    # return jsonify(role=True)
    content = request.get_json()
    # return content
    conn = db_connect()
    user_name = content['username']
    Password = content['password']

    # user_name = username
    # Password = password

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Users where User_Name = %s AND Password = %s', (user_name, Password))
        result = cursor.fetchall()
        if len(result) == 1:
            for row in result:
                role = row['User_Type']
                conn.close()

                if role == 'Buyer':
                        return jsonify(auth_success = True,role ="Buyer")

                elif role == 'Seller':
                    return jsonify(auth_success = True,role ="Seller")
                elif role == 'Admin':
                    return jsonify(auth_success = True,role ="Admin")
        else:
            return jsonify(auth_success = False)


@app.route("/android_buyer_home", methods = ['POST', 'GET'])
def android_buyer_home():
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Inventory_Items where Available_From <= %s', date.today())
        items = cursor.fetchall()
    conn.close()
    return jsonify(items)


@app.route("/android_calculate_price", methods = ['POST', 'GET'])
def android_calculate_price():
   # return jsonify(role=True)
   content = request.get_json()
   # return content
   conn = db_connect()
   Item_ID = content['item_id']
   days = content['days']
   with conn.cursor() as cursor:
       cursor.execute('Select * from Inventory_Items where Item_ID= %s',Item_ID)
       items = cursor.fetchall()
       for item in items:
           rental_price = float(item['Rental_Price'])
           deposit = float(item['Deposit'])
   total_price = deposit + (float(days) * rental_price)
   conn.close()
   price = str(total_price)
   return jsonify(price=price)

@app.route("/android_place_order", methods = ['POST', 'GET'])
def android_place_order():
   # return jsonify(role=True)
   content = request.get_json()
   Item_ID = content['item_id']
   user_name = content['user_name']
   days = int(float(content['days']))
   shipping_address = content['shippingaddress']
   delivery_date = date.today() + timedelta(days=7)
   days = int(days)
   return_date = delivery_date + timedelta(days=days)
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute('Select * from Users where user_name = %s', user_name)
       items = cursor.fetchall()
       for item in items:
           User_ID = item['User_ID']
           conn.close()
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute(
           'INSERT INTO Orders(User_ID, Item_ID, Delivery_Date, Return_Date, Shipping_Address, Order_Status) VALUES(%s,%s,%s,%s,%s,%s)',
           (User_ID, Item_ID, delivery_date, return_date, shipping_address, "Order Received(Shipment Pending)"))
       conn.commit()
       conn.close()
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute('Update Inventory_Items set Available_From = NULL where Item_ID=%s ', Item_ID)
       conn.commit()
       conn.close()
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute('SELECT * FROM Orders where User_Id = %s AND Item_ID = %s', (User_ID, Item_ID))
       orders = cursor.fetchall()
       for order in orders:
           orderid = order['Order_ID']
       conn.close()
       return jsonify(order_id = orderid)

@app.route("/android_signup", methods=['POST', 'GET'])
def signup_user():
    content = request.get_json()
    conn = db_connect()

    User_Name = content['user_name']
    Password = content['password']
    User_Type = "Buyer"
    First_Name = content['first_name']
    Last_Name = content['last_name']
    Email = content['email']
    Address = content['address']
    Phone_Num = content['contact']

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Users where User_Name = %s', User_Name)
        result = cursor.fetchall()
        if len(result) > 0:
            conn.close()
            return jsonify(auth_success = False, message = "Failed")

    with conn.cursor() as cursor:
        cursor.execute('Insert into Users(User_Name, Password, User_Type, First_Name, Last_Name, Email, Address, Phone_Num) values(%s,%s,%s,%s,%s,%s,%s,%s)',
                        (User_Name, Password, User_Type, First_Name, Last_Name, Email, Address, Phone_Num))
        conn.commit()
        conn.close()

    return jsonify(auth_success = True, message = "Succeeded")

@app.route('/android_myorders',methods = ['POST','GET'])
def android_check_my_orders():

    content = request.get_json()
    conn = db_connect()

    user_name = content['user_name']

    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Users where User_Name = %s',user_name)
        users = cursor.fetchall()
        conn.close()
    for user in users:
        user_id = user['User_ID']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Orders where User_ID = %s', user_id)
        orders = cursor.fetchall()
        conn.close()

    return jsonify(orders)

@app.route('/android_return_item',methods = ['POST','GET'])
def android_return_item():
    content = request.get_json()
    Order_ID = content['Order_ID']
    Item_ID = content['Item_ID']
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from Orders where Order_ID = %s',Order_ID)
        orders = cursor.fetchall()
        conn.close()
        for order in orders:
            orderstatus = order['Order_Status']

        if orderstatus == "Order Shipped":
            conn = db_connect()
            with conn.cursor() as cursor:
                cursor.execute('Update Orders set Order_Status = "Order Returned",Actual_Return_Date=%s where Order_ID = %s',(date.today(),Order_ID))
                conn.commit()
                conn.close()
                conn = db_connect()
                with conn.cursor() as cursor:
                    cursor.execute('Update Inventory_Items set Available_From = %s where Item_ID = %s',(date.today(),Item_ID))
                    conn.commit()
                    conn.close()
            return jsonify(auth_success = True, message = "Succeeded")
        else:
            return jsonify(auth_success = False, message = "Failed")

@app.route('/android_rent_item', methods = ['POST', 'GET'])
def android_rent_item():

    content = request.get_json()
    user_name = content['User_Name']
    item_id = content['Item_ID']
    rent_days = content['Rent_Days']
    shipping_address = content['Shipping_Address']

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Inventory_Items where Item_ID= %s', item_id)
        items = cursor.fetchall()
        for item in items:
            rental_price = float(item['Rental_Price'])
            deposit = float(item['Deposit'])
    total_price = deposit + (float(rent_days) * rental_price)
    conn.close()
    price = str(total_price)

    delivery_date = date.today() + timedelta(days=7)
    days = int(rent_days)
    return_date = delivery_date + timedelta(days=days)
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Users where user_name = %s', user_name)
        items = cursor.fetchall()
        for item in items:
            User_ID = item['User_ID']
            conn.close()
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Orders(User_ID, Item_ID, Delivery_Date, Return_Date, Shipping_Address, Order_Status) VALUES(%s,%s,%s,%s,%s,%s)',
            (User_ID, item_id, delivery_date, return_date, shipping_address, "Order Received(Shipment Pending)"))
        conn.commit()
        conn.close()
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Update Inventory_Items set Available_From = NULL where Item_ID=%s ', item_id)
        conn.commit()
        conn.close()
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Orders where User_Id = %s AND Item_ID = %s', (User_ID, item_id))
        orders = cursor.fetchall()
        for order in orders:
            orderid = order['Order_ID']
        conn.close()
        return jsonify(auth_success = True, message = "Succeeded")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

