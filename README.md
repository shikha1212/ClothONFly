# Cloth-ON-Fly

Cloth ON Fly is a clothing rental platform. Some people always have idle clothes staying in their shelf. Some other people always have the occasions that needs some clothes, but there is no appropriate clothes in their shelf. Cloth ON Fly is here to help. Buyers could rent clothes with us at a fraction of their original price. Sellers could put the clothes on our platform for renting. We also designed the access for Admin people to manage the whole website. Backend of the project is created using Python. The webapp was launched using Google App Engine; all of the data is stored in App Engine's Datastore, and the images were stored in GAE's Cloud Storage buckets. We also deploy an Android App using Kotlin by connecting with the web app.

Detailed Introduction could be found here: [Introduction to Cloth ON Fly](http://cloth-on-fly.appspot.com/info)

## Operations

1. User Signup (Buyer/Seller/Admin)
2. User Login (Buyer/Seller/Admin)
3. Add a new clothing item (Seller)
4. Remove an existing clothing item (Seller/Admin)
5. Display all available clothing items (Buyer)
6. Rent an item – system creates an order in orders table (Buyer)
7. Calculate and display total price of the order  (Buyer)
8. Display all orders placed by a buyer (Buyer)
9. Ship an item (Seller)
10. Return an item (Buyer)
11. Refund the deposit (Seller)
12. Withhold the deposit (Seller)
13. Remove an existing user (Admin)
14. Logout

## Products

* Click the link here to access our web app

  [Cloth ON Fly WEB APP](http://cloth-on-fly.appspot.com/)

* Using android phone to click the link to download

  [Cloth ON Fly ANDROID APP .apk](https://storage.cloud.google.com/clothonfly_bucket/app-debug.apk)

## Languages

* [Python][1]
* [HTML][2] 
* [CSS][3]
* [Kotlin][4]
* [XML][5]
* [Cloud SQL][6]
* [Sqlite3][7]

## APIs

* [Users API][8]
* [cloudstorage API][9]
* [Pymysql API][10]

## Dependencies

* [Googla App Engine][11]
* [Flask][12]
* [jinja2][13]
* [Okhttp][14]
* [Materialize][15]

## Team

* [Tianyi (Kelly) Zhang](https://www.linkedin.com/in/kellytianyizhang/) 
* [Shikha Singh](https://www.linkedin.com/in/shikhasingh1212/)



[1]: https://python.org
[2]: https://www.w3schools.com/html/default.asp
[3]: https://www.w3schools.com/css/default.asp
[4]: https://kotlinlang.org/
[5]: https://www.w3schools.com/xml/xml_whatis.asp
[6]: https://cloud.google.com/sql/docs/
[7]: https://www.sqlite.org/index.html
[8]: https://developers.google.com/appengine/docs/python/users/
[9]: https://cloud.google.com/appengine/docs/standard/python/cloud-sql/using-cloud-sql-mysql
[10]: https://github.com/PyMySQL/PyMySQL
[11]: https://developers.google.com/appengine
[12]: https://flask.palletsprojects.com/en/1.1.x/
[13]: http://jinja.pocoo.org/docs/
[14]: https://square.github.io/okhttp/
[15]: https://getmdl.io/