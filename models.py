from peewee import *
import datetime 
from datetime import date

db = SqliteDatabase("models.db")

# product description

class Product(Model):
    price_per_unit =     DecimalField(decimal_places = 2,auto_round=True)
    product_id =         IntegerField(unique=True)
    quantity_in_stock =  IntegerField()
    product_name =       CharField()
    description =        CharField()

    class Meta:
        database = db 

# tags per product

class Tags_per_Product(Model):
    product_id = ForeignKeyField(Product, backref='product_tags')
    tag_id =     IntegerField()
    
# id tag description

class Tag_id (Model):
    tag_id =   ForeignKeyField(Tags_per_Product, backref='tag_id',unique=True)
    tag_name = CharField(unique=True)
    
# Product per seller 

class Seller_per_product (Model):
    product = ForeignKeyField(Product, backref='seller_product',unique=True)
    user_id = IntegerField()
  
    class Meta:
        database = db

# user description

class User(Model):
    user_id =             ForeignKeyField(Seller_per_product, backref='user_id') 
    user_name =           CharField()
    address_data =        CharField()
    billing_information = CharField()

    class Meta:
        database = db

# transation description

class Purchase_history(Model):
    buyer_id =         ForeignKeyField(User, backref='buyer_purchases')
    seller_id =        ForeignKeyField(User, backref='seller_purchases')
    purchase_product = ForeignKeyField(Product, backref='purchases')
    purchase_id =      IntegerField(unique=True)
    purchase_date =    DateTimeField()
    products_sent =    BooleanField()
    bill_payed =       BooleanField()
 
    class Meta:
        database = db

db.connect()

db.create_tables([Product,Tags_per_Product,Tag_id,Seller_per_product,User,Purchase_history])

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