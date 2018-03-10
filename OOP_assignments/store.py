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

    def inventory(self):
        self.info()
        print "\n" + "-"*25 + "Inventory" + "-"*25
        for product in range(len(self.products)):
            print "{} {}\n\tPrice: {}, \tSale Price: {}".format(self.products[product]['brand'], self.products[product]['item'], self.products[product]['price'], self.products[product]['sale_price'])
        return self

    def brand_sale(self, brand, percent):
        if type(percent) == int:  #if percent entered as integer, convert to decimal
            percent = float(percent)/100
        for product in range(len(self.products)):
            if self.products[product]['brand'] == brand: #apply the sale
                self.products[product]['sale_price'] = Decimal(self.products[product]['price'] - (self.products[product]['price'] * percent)).quantize(Decimal('0.01', Decimal._round_half_up))

#create some products
shoes1 = Product(89.99, 'Janissah Wedge Sandals', '9 oz', 'Nine West', color='Taupe')
shoes2 = Product(89.00, 'Emmala', '7 oz', 'Nine West', color='Orange Multi')
shoes3 = Product(59.99, 'Longitano Sandals', '9 oz', 'Nine West', color='Black Silver')
shoes4 = Product(210.00, 'Hallden', '9 oz', 'Ted Baker', color='Palace Gardens')
shoes5 = Product(169.59, 'Rashi', '8 oz', 'Imagine Vince Camuto', color='Soft Gold')
shoes6 = Product(39.99, 'Rainaa', '9 oz', 'Bandolino', color='Gold Glamour')
shoes7 = Product(47.99, 'Rainaa', '9 oz', 'Bandolino', color='Gunmetal Glamour')
shoes8 = Product(84.95, 'Faelyn', '8 oz', 'Anne Klein', color='Tropical Black Multi')
shoes9 = Product(328.00, 'Licorice Too', '7 oz', 'Kate Spade', color='Multi Glitter')
shoes10 = Product(109.00, 'Ginette', '9 oz', 'Calvin Klein', color='Sandstorm')
shoes11 = Product(777.00, 'Sequined Pumps', '10 oz', 'Dolce & Gabbana', color='Black')
purse1 = Product(228.00, 'Kingston Drive Blossom Alessa', '13 oz', 'Kate Spade', color='Cream multi')
purse2 = Product(98.00, 'Blake Street Ditsy Blossom Mikey', '3 oz', 'Kate Spade', color='Black')
purse3 = Product(98.00, 'Blake Street Ditsy Blossom Mikey', '3 oz', 'Kate Spade', color='Watermelon')
purse4 = Product(117.99, 'Novelty East/West Boxed', '1 lb 10.8 oz', 'Calvin Klein', color='Cashew')
purse5 = Product(54.99, 'Card Holder', '2.6 oz', 'Michael Kors', color='Light Pewter')
purse6 = Product(54.99, 'Card Holder', '2.6 oz', 'Michael Kors', color='Soft Pink')

#create a store
store1 = Store("Shannon's Shoemania", "Shannon Steen", "4325 S. Front St, Wilmington NC")
store1.add_product(shoes1).add_product(shoes2).add_product(shoes3).add_product(shoes4).add_product(shoes5).add_product(shoes6).add_product(shoes7).add_product(shoes8).add_product(shoes9).add_product(shoes10).add_product(shoes11).add_product(purse1).add_product(purse2).add_product(purse3).add_product(purse4).add_product(purse5).add_product(purse6)
store1.inventory()
store1.brand_sale('Kate Spade', 20)
store1.inventory()
