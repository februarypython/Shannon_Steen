''' OOP Assignment 1 - Bike:
Create a new class called Bike with the following:
    Attributes: price, max_speed, miles (default to 0)
    Methods:
        displayInfo() - have this method display the bike's price, maximum speed, and the total miles.
        ride() - have it display "Riding" on the screen and increase the total miles ridden by 10
        reverse() - have it display "Reversing" on the screen and decrease the total miles ridden by 5

Create 3 instances of the Bike class.
    Have the first instance ride three times, reverse once and have it displayInfo().
    Have the second instance ride twice, reverse twice and have it displayInfo().
    Have the third instance reverse three times and displayInfo().

Prevent the instance from having negative miles. '''

class Bike(object):
    def __init__(self, price, max_speed):
        self.price = price
        self.max_speed = max_speed
        self.miles = 0
    
    def displayInfo(self):
        print "Price: ${}".format(self.price)
        print "Maximum Speed: {}mph".format(self.max_speed)
        print "Total Miles: {}".format(self.miles)
        return self

    def ride(self):
        print "...Riding"
        self.miles += 10
        return self
    
    def reverse(self):
        if self.miles >= 5:
            print "Reversing..."
            self.miles -= 5
        return self

red_bike = Bike(50, 5)
red_bike.ride().ride().ride().reverse().displayInfo()

blue_bike = Bike(100, 22)
blue_bike.ride().ride().reverse().reverse().displayInfo()

brown_bike = Bike(5, 2)
brown_bike.reverse().reverse().reverse().displayInfo()