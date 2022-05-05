from peewee import *
from datetime import date
from models import *

db = SqliteDatabase("tables.db")


db.connect()

db.create_tables([Product,User,Tags_per_Product,Seller_per_product,Purchase_history])

Product.create(price_per_unit = 3.2,
               product_id = 1398,
               quantity_in_stock = 23,
               product_name = "focaccia",
               description = "Italian bread")

User.create(user_id = 31321,
            user_name = "Charlie",
            address_data ="Koningstraat 41",
            billing_information = "Koningstraat 41 4322 LD, Amsterdam\n0613552485")

Tags_per_Product.create(product_id = 1398, tag_id = 2498)

Seller_per_product.create(user_id = "43256", product = 1398)

Purchase_history.create(purchase_id = 35345, 
                        buyer_id = 734567, 
                        seller_id = 345633, 
                        purchase_date = date(2022, 4, 29), 
                        purchase_product = 1398, 
                        purchase_quantity = 2, 
                        products_sent = True, 
                        bill_payed = True)


db.close