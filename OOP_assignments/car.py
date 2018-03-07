''' OOP Assignment 2 - Car:
Create a class called  Car. In the__init__(), allow the user to specify the following attributes: price, speed, fuel, mileage. If the price is greater than 10,000, set the tax to be 15%. Otherwise, set the tax to be 12%. 

Create six different instances of the class Car. In the class have a method called display_all() that returns all the information about the car as a string. In your __init__(), call this display_all() method to display information about the car once the attributes have been defined.'''

class Car(object):
    def __init__(self, price, speed, fuel, mileage):
        self.price = price
        self.speed = speed
        self.fuel = fuel
        self.mileage = mileage
        if self.price > 10000:
            self.tax = 0.15
        else:
            self.tax = 0.12
        self.display_all()
        
    def display_all(self):
        print "Price: ${}".format(self.price)
        print "Speed: {}".format(self.speed)
        print "Fuel: {}".format(self.fuel)
        print "Mileage: {}mpg".format(self.mileage)
        print "Tax: {}".format(self.tax)
        return self

black_aura = Car(8000, 55, 'almost empty', 22)
blue_explorer = Car(4500, 40, 'half a tank', 15)
wine_rav4 = Car(12000, 45, 'empty', 34)
red_charger = Car(22000, 75, 'full', 12)
blue_accord = Car(9800, 60, 'mostly full', 29)
silver_audi = Car(10500, 45, 'more than half', 28)