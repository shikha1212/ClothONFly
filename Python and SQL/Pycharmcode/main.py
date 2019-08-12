import sqlite3


def calculate_price(id_num, rent_days):
    db = sqlite3.connect("ClothONFly.db")
    cursor = db.cursor()
    cursor.execute('''select Rental_Price,Deposit from Inventory_Items where Item_ID= ?''', (str(id_num)))
    for row in cursor.fetchall():
        rental_price = row[0]
        deposit = row[1]
    total_price = float(deposit) + (int(rent_days) * int(rental_price))
    return total_price

print(str(calculate_price('1','3')))

