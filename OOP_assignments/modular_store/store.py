''' OOP Assignment 9 - Store
Build a store to contain our products by making a store class and putting our products into an array.
    ATTRIBUTES: products (array of products objects); location (store address); owner (store owner's name)
    METHODS:
        add_product: add a product to the store's product list
        remove_product: should remove a product according to the product name
        inventory: print relevant information about each product in the store: '''

# Additional features outside of assignment requirements:
#       Added info method to display store info
#       Added brand_sale method to apply sale price to all products of given brand
#       Added remove_sale method to remove sale price from all products of given brand
#       Added search_brand method to search for all inventory items of given brand

 
from product import Product  #import Product class (created in assignment 4)
from decimal import Decimal 

class Store(object):
    def __init__(self, name, owner, address):
        self.store = name 
        self.owner_name = owner
        self.address = address
        self.products = []

    def add_product(self, product):
        self.products.append({'item': product.item_name, 'brand': product.brand, 'weight': product.weight, 'price': product.price, 'status': product.status, 'sale_price': 'n/a'})
        return self

    def remove_product(self, item):
        for product in range(len(products)):
            if self.products[product]['item'] == item:
                idx = [product]  #found the product, break out of loop and remove from inventory
                break
            self.products.pop(idx)
            return self

    def info(self):
        print "\n" + "="*70
        print "Name: {}\nOwner: {}\n{}".format(self.store, self.owner_name, self.address)
        return self

    def inventory(self):
        self.info()
        print "\n" + "-"*25 + "Inventory" + "-"*25
        for product in range(len(self.products)):
            print "\n{} {}\n\tPrice: {}, \tSale Price: {}".format(self.products[product]['brand'], self.products[product]['item'], self.products[product]['price'], self.products[product]['sale_price'])
        return self

    def search_brand(self, brand):  #search inventory for specific brand
        self.info()
        found = False
        for product in range(len(self.products)):
            if self.products[product]['brand'] == brand:
                print "\n{} {}\n\tPrice: {}, \tSale Price: {}".format(self.products[product]['brand'], self.products[product]['item'], self.products[product]['price'], self.products[product]['sale_price'])
                found = True
        if not found:
            print "We're sorry. We do not have any {} in stock at this time.".format(brand)

    def brand_sale(self, brand, percent):
        if type(percent) == int:  #if percent entered as integer, convert to decimal
            percent = float(percent)/100
        for product in range(len(self.products)):
            if self.products[product]['brand'] == brand: #apply the sale
                self.products[product]['sale_price'] = Decimal(self.products[product]['price'] - (self.products[product]['price'] * percent)).quantize(Decimal('0.01', Decimal._round_half_up))

    def remove_sale(self, brand):
        for product in range(len(self.products)):
            if self.products[product]['brand'] == brand: #remove the sale
                self.products[product]['sale_price'] = 'n/a'

#test code
if __name__ == "__main__":
    store1 = Store("Shannon's Shoemania", "Shannon Steen", "4325 S. Front St, Wilmington NC")
    store1.info()
