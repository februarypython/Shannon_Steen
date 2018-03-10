from decimal import Decimal 
class Product(object):
    def __init__(self, price, name, weight, brand, **kwargs):
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

#test code
if __name__ == "__main__":
    shoes1 = Product(89.99, 'Janissah Wedge Sandals', '9 oz', 'Nine West', color='Taupe')
    shoes1.display_info()
    shoes1.sell()
    shoes1.display_info()