from models import *
from peewee import JOIN
import sys
import os

def main():
    print("Welcome to the inventory check of Betsy's marketplace.\nPlease select the function that you wish to perform.")
    while True:
        print_menu()
        choice = get_menu_choice()
        if choice == 1:
            search()
        elif choice == 2:
            all_user_products()
        elif choice == 3:
            list_products_off_tag()
        elif choice == 4:
            add_product()
        elif choice == 5:
            remove_product()
        elif choice == 6:
            update_stock()
        elif choice == 7:
            handle_purchase()
        elif choice.upper() == "Q":
            break

def print_menu():
    print("1: Search for a specific product")
    print("2: Print all of the products of a user")
    print("3: Print all of the products of a tag")
    print("4: Add a product to a user")
    print("5: Remove a product from a user")
    print("6: Update the stock quantity of a product.")
    print("7: Handle a purchase")

def get_menu_choice():
    choice = input("\nPlease choose an option (1-8) or press 'Q' to quit: ")
    while choice.isnumeric() is False and choice.upper() != "Q":
        choice = input("Please choose an option (1-8) or press 'Q' to quit: ")
    if choice.isnumeric():
        choice = int(choice)
    return choice

def search(word):
    search_bar = Product.select(Product.product_id,Product.product_name,Product.description,Product.price_per_unit,Product.quantity_in_stock).where((Product.product_name.contains(word)) | (Product.description.contains(word)))
    x = [] 
    for product in search_bar:
        x.append((product.product_id,product.product_name,product.description))
    return x

def all_user_products(tag_id):
    query = Tags_per_Product.select(Tags_per_Product.tag_id,Tag_id.tag_name,Product.product_id,Product.product_name,Product.description)\
            .join(Tag_id, on= Tag_id.tag_id == Tags_per_Product.tag_id, attr="tags")\
            .switch(Tags_per_Product)\
            .join(Product, on=Tags_per_Product.product_id == Product.product_id, attr="product_id")\
            .where(tag_id==Tags_per_Product.tag_id)
    x = [] 
    for product in query: 
        x.append((product.tag_id, product.tags.tag_name, product.product_id.product_id, product.product_id.product_name, product.product_id.description))

    return x

def list_products_off_tag(tag_id):
    query = Tags_per_Product.select(Tags_per_Product.tag_id,Tag_id.tag_name,Product.product_id,Product.product_name,Product.description)\
            .join(Tag_id, on= Tag_id.tag_id == Tags_per_Product.tag_id, attr='tags')\
            .switch(Tags_per_Product)\
            .join(Product, on=Tags_per_Product.product_id == Product.product_id, attr='product_id')\
            .where(tag_id==Tags_per_Product.tag_id)
    x=[]
    for product in query: 
        x.append((product.tag_id, product.tags.tag_name, product.product_id.product_id, product.product_id.product_name, product.product_id.description))
    return x

def find_last_id():
    query = Product.select(Product.product_id).order_by(Product.product_id.desc())
    for product in query:
        return product.product_id

def add_product(user_id,product_name,product_description,price,quantity,tag1,tag2):
  try:
        find_last_id
        a = Product.insert(product_id=(find_last_id()+1),product_name=product_name,description=product_description,price_per_unit=price,quantity_in_stock=quantity)
        a.execute()
        b = Seller_per_product.insert(user_id = user_id,product = (find_last_id()))
        b.execute()
        c = Tags_per_Product.insert(product_id=(find_last_id()),tag_id=tag1)
        c.execute()
        d = Tags_per_Product.insert(product_id=(find_last_id()),tag_id=tag2)
        d.execute()
        return "Product added."
    except: return "ERROR."


def remove_product(product_id):
    try:
        a =Product.delete().where(Product.product_id == product_id)
        a.execute()
        b=Tags_per_Product.delete().where(Tags_per_Product.product_id == product_id)
        b.execute()
        c=Seller_per_product.delete().where(Seller_per_product.product == product_id)
        c.execute()
        return "Product removed."
    except: return "ERROR."

def update_stock(product_id, new_quantity):
    try:
        update = Product.update(quantity_in_stock = new_quantity).where(Product.product_id == product_id)
        update.execute()
        return "Stock is updated"
    except: return "ERROR."

def return_last_product_quantity(product_id):
    query = Product.select(Product.product_id,Product.quantity_in_stock).where(Product.product_id == product_id)
    for product in query:
        return product.quantity_in_stock

def return_last_transaction_id():
    query = Purchase_history.select(Purchase_history.transaction_id).order_by(Purchase_history.transaction_id.desc())
    for transaction in query:
        return transaction.transaction_id


def return_user_id(product_id):
    query = Seller_per_product.select(Seller_per_product.user_id,Seller_per_product.product).where(Seller_per_product.product_id == product_id)
    for user in query:
        return(user.user_id)


def handle_purchase(product_id, buyer_id, quantity):
    try:
        new_quantity = (return_last_product_quantity(product_id))-quantity 
        if new_quantity >= 0:
            update_stock(product_id,new_quantity)
            today= datetime.today().strftime("%Y-%m-%d")
            a = Purchase_history.insert(transaction_id=(return_last_transaction_id()+1),customer_id=buyer_id,seller_id= return_user_id(product_id),\
                purchase_date = today, purchase_product= product_id, purchase_quantity=quantity, customer_invoice_sent= "FALSE", customer_invoice_payed= "FALSE")
            a.execute()
            return "Product is being purchased."
        else: return "Not enough in stock."
    except: return "ERROR."

        
if __name__ == "__main__":
    main()





