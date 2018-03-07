''' OOP Assignment 4 - Product
The owner of a store wants a program to track products. 
Create a product class to fill the following requirements:
    Attributes: Price, Item Name, Weight, Brand, Status: default "for sale"
    Methods:
        Sell: changes status to "sold"
        Add tax: takes tax as a decimal amount as a parameter and returns the price of the item including sales tax
        Return: takes reason for return as a parameter and changes status accordingly. If the item is being returned because it is defective, change status to "defective" and change price to 0. If it is being returned in the box, like new, mark it "for sale". If the box has been, opened, set the status to "used" and apply a 20% discount.
        Display Info: show all product details. '''

from decimal import Decimal 
class Product(object):
    def __init__(self, price, name, weight, brand):
        self.price = price
        self.item_name = name
        self.weight = weight
        self.brand = brand
        self.status = "For Sale"

    def sell(self):
        self.status = "Sold"
        return self
    
    def add_tax(self, tax):
        if type(tax) == float: 
            self.price = Decimal(self.price + (self.price * tax)).quantize(Decimal('0.01', Decimal._round_half_up))
        elif type(tax) == int:
            tax = float(tax)/100
            self.price = Decimal(self.price + (self.price * tax)).quantize(Decimal('0.01', Decimal._round_half_up))
        else:
            self.price = self.price
        return self.price
    
    def returned(self, reason):
        if reason == "defective" or reason == 'broken':
            self.price = 0
            self.status = "Defective"
        elif reason == "unopened" or reason == "like new":
            self.status = "For Sale"
        else:
            self.price = Decimal(self.price - (self.price * .20)).quantize(Decimal('0.01', Decimal._round_half_up))
            self.status = "Used"
        return self
    
    def display_info(self):
        print "Product Details"
        print "Item Name: {}".format(self.item_name)
        print "Brand: {}".format(self.brand)
        print "Status: {}".format(self.status)
        print "Price: ${}".format(self.price)
        print "Weight: {}".format(self.weight)
        return self

ereader = Product(99.99, 'e-reader', '7.2 oz', 'Kindle')
headphones = Product(42.99, 'wireless headphones', '4.8 oz', 'COWIN')
groomer = Product(10, 'pet grooming brush', '4.8 oz', 'Excell Electronics')
projector = Product(75.18, 'LED projector', '3.3 lbs', 'DBPower')

projector.add_tax(.12) 
projector.sell().display_info()  #should change status to Sold, price to $84.20
print "="*100
ereader.add_tax(.16) 
ereader.sell().returned('defective').display_info() #should change price to $0, status to defective
print "="*100
groomer.add_tax(8)  
groomer.sell().returned('unopened').display_info() #should show status "for sale", price $10.80
print "="*100
headphones.add_tax('tax free day') 
headphones.sell().returned('did not like').display_info() #should show status used, price should be $34.39