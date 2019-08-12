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
import os
from flask import Flask, request, render_template
from datetime import date, datetime,timedelta

import pymysql


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__,template_folder='template')
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

@app.route("/")
def home():
    return render_template('login.html')

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
                        conn = db_connect()
                        with conn.cursor() as cursor:
                            cursor.execute('Select * from Inventory_Items where Available_From <= %s',date.today())
                            items = cursor.fetchall()
                        conn.close()
                        return render_template("buyerhome.html", items=items, user_name = user_name)
                    elif role == 'Seller':
                        return render_template('sellerhome.html', user_name = user_name)
                    elif role == 'Admin':
                        return render_template('adminhome.html', user_name = user_name)
            else:
                return render_template("login.html")

    elif request.form['action'] == "Sign Up":
        return render_template('register.html')


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
        cursor.execute('Insert into Users(User_Name, Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num) values(%s,%s,%s,%s,%s,%s,%s,%s)',
                        (User_Name, Password,User_Type,First_Name,Last_Name,Email,Address,Phone_Num))
        conn.commit()
        conn.close()

    return render_template('login.html')

@app.route("/itemadded", methods=['POST'])
def item_added():

    fp = open(request.form['image'])
    img = fp.read()
    fp.close()

    Brand_Name = request.form['brand'],
    Cloth_Type = request.form['type']
    Size = request.form['size'],
    Gender = request.form['gender'],
    Original_Price = request.form['original_price'],
    Rental_Price = request.form['rental_price'],
    Owner_ID = request.form['Owner_ID'],
    Location = request.form['location'],
    Cloth_Image = img,
    Deposit= request.form['deposit'],
    Available_From = date.today()

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Insert into Inventory_Items(Brand_Name, Cloth_Type, Size, Gender, Original_Price, Rental_Price, Owner_ID, Location, Cloth_Image, Deposit, Available_From) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (Brand_Name, Cloth_Type, Size, Gender, Original_Price, Rental_Price, Owner_ID, Location, Cloth_Image, Deposit, Available_From))
    conn.commit()
    conn.close()
    return "Item added"

@app.route("/buyerhome", methods=['POST'])
def buyerhome():
    return render_template('buyerhome.html')

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

@app.route('/confirm_order/<string:Item_ID>/<string:user_name>/<string:days>',methods = ['POST','GET'])
def confirm_order(Item_ID,user_name,days):
    user_name = user_name
    shipping_address = request.form['address']
    delivery_date = date.today() + timedelta(days=7)
    days = int(float(days))
    return_date = delivery_date + timedelta(days=days)
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('Select * from Users where user_name = %s',user_name)
        items = cursor.fetchall()
        conn.close()
        for item in items:
            User_ID = item['User_ID']
    Item_ID = Item_ID

    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Orders(User_ID, Item_ID, Delivery_Date, Return_Date, Shipping_Address, Order_Status) VALUES(%s,%s,%s,%s,%s,%s)',
                        (User_ID,Item_ID,delivery_date,return_date,shipping_address,"Order Received(Shipment Pending)"))
        conn.commit()

        cursor.execute('Update Inventory_Items set Available_From = NULL where Item_ID=%s ',Item_ID)
        conn.commit()
        cursor.execute('SELECT * FROM Orders where User_Id = %s AND Item_ID = %s',(User_ID,Item_ID))
        items = cursor.fetchall()
        for item in items:
            Order_ID = item['Order_ID']

        conn.close()

    return "Order Confirmed !! Order ID: " + Order_ID

@app.route("/adminremoveu", methods=['POST','GET'])
def adminremoveu():
    return render_template("userremoved.html")

@app.route("/adminremovei", methods=['POST','GET'])
def adminremovei():
    return render_template("itemremoved.html")

@app.route("/userremoved", methods=['POST','GET'])
def remove_user():
   User_Name = request.form['user_name']
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute('DELETE FROM Users WHERE User_Name = %s', User_Name)
   conn.commit()
   conn.close()
   return "User Removed"

@app.route("/itemremoved", methods=['POST','GET'])
def remove_item():
   Item_ID = request.form['item_id']
   conn = db_connect()
   with conn.cursor() as cursor:
       cursor.execute('DELETE FROM Inventory_Items WHERE Item_ID = %s', Item_ID)
   conn.commit()
   conn.close()
   return "Item Removed"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

