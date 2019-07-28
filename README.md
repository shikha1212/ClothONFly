# ClothONFly
Rental clothing application

Narrative: 
ClothONFLY is a clothing rental platform. ClothONFLY lets you rent clothes at a fraction of their original price.

Things of Interest:
1.	Admins - Admin manages the site 
2.	Seller – A seller can add their clothing items on the platform for renting.
3.	Order – These are the orders placed by the buyers
4.	Clothing Items – These are the items that available for renting
5.	Buyer – A buyer can rent any available item from the platform by paying a deposit amount plus the rental price

Business Rules:
1.	An admin will authorize sellers on the platform
2.	Any user can register as a buyer on the platform
3.	Clothing Items are available from the date it is added on the system unless explicitly specified by the seller
4.	Delivery Date of all rented items will be Current Date plus 7 days
5.	Clothing item that has been rented out will not be available for renting till returned
6.	Every clothing item will have a deposit amount and rental price per day as decided by the seller.
7.	A buyer can rent any available item by paying the deposit amount plus the rental price (rental price per day * no. of days for which the item is rented). 
a)	The buyer has to enter a return date by when he/she will return the product back to seller. 
b)	The buyer has to return the item by the return date he has specified in the order, failing to do so will let the seller withhold the deposit paid by the user.
c)	If the item is returned by the return date, the seller refunds the deposit amount and item is available for renting again



Operations:
1.	Buyer Registration
2.	Seller Registration
3.	Admin Registration
4.	User Login (Buyer/Seller/Admin)
5.	Add a new clothing item (Seller/Admin)
6.	Add clothing items in bulk
7.	Update an existing clothing item (Seller/Admin)
8.	Remove an existing clothing item (Seller/Admin)
9.	Display all available clothing items (Buyer)
10.	Rent an item – system creates an order in orders table (Buyer)
11.	Calculate and display total price of the order
12.	Display all orders placed by a buyer (Buyer)
13.	Ship an item (Seller)
14.	Return an item (Buyer)
15.	Refund the deposit (Seller)
16.	Withhold the deposit (Seller)
17.	Display and Export(csv) all orders details including buyer, seller, item and order details (Admin)
18.	Display and Export(csv) all orders for a seller (buyer, item and order details)
19.	Logout


