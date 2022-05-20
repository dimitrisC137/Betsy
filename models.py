from peewee import *
import datetime 
from datetime import date
from tables import *

db = SqliteDatabase("models.db")

# product description
class User(BaseModel):
    user_id =             ForeignKeyField(Seller_per_product, backref='user_id') 
    user_name =           CharField()
    address_data =        CharField()
    billing_information = CharField()

class BaseModel(Model):
    class Meta:
        database = db

class Product(BaseModel):
    price_per_unit =     DecimalField(decimal_places = 2,auto_round=True)
    product_id =         IntegerField()
    quantity_in_stock =  IntegerField()
    product_name =       CharField()
    description =        CharField()
# tags per product

class Tags_per_Product(BaseModel):
    product_id = ForeignKeyField(Product, backref='product_tags')
    tag_id   =   ForeignKeyField(Product, backref='tag_id',unique=True)
    tag_id =     IntegerField()
    
# id tag description

class Tag_id (BaseModel):
    tag_name = CharField(unique=True)
    
# Product per seller 

class Seller_per_product (BaseModel):
    product = ForeignKeyField(Product, backref='seller_product',unique=True)
    user_id = IntegerField()

# user description

# transation description

class Purchase_history(BaseModel):
    buyer_id =         ForeignKeyField(User, backref='buyer_purchases')
    seller_id =        ForeignKeyField(User, backref='seller_purchases')
    purchase_product = ForeignKeyField(Product, backref='purchases')
    purchase_id =      IntegerField(unique=True)
    purchase_date =    DateTimeField()
    products_sent =    BooleanField()
    bill_payed =       BooleanField()
 
