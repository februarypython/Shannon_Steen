''' OOP Assignment 5 - Animal
Create an Animal class
    ATTRIBUTES: name, health
    METHODS: walk() decreases health by 1; run() decreases health by 5; display_health()

Create an Dog class
    ATTRIBUTES: inherits from animal, default health to 150
    METHODS: pet() increases health by 5

Create an Dragon class
    ATTRIBUTES: inherits from animal, default health to 170
    METHODS: fly() increases health by 10; when display_health() called, also print "I am a Dragon" '''

#create parent Animal class with attributes of name, health and methods of walk, run, display_health
class Animal(object):
    def __init__(self, name, health):
        self.name = name
        self.health = health
    def walk(self):
        if self.health >= 1: #preventing negative health
            self.health -= 1
        return self
    def run(self):
        if self.health >= 5: #preventing negative health
            self.health -= 5
        return self
    def display_health(self):
        print "Remaining health: {}".format(self.health)
        return self

#create an Animal
cat = Animal('cat', 20)
print cat.name
cat.walk().walk().walk().run().run().display_health() #should print 7, should not inlude "I am a Dragon"
# cat.pet() #should not be allowed
# cat.fly() #should not be allowed

#create a Dog class that inherits Animal attributes/methods, default health=150, pet method increases health by 5
class Dog(Animal):
    def __init__(self, name, health=150):
        super(Dog, self).__init__(name, health)
    def pet(self):
        self.health += 5
        return self

#create a Dog
dog1 = Dog('fluffy')
print dog1.name
dog1.walk().walk().walk().run().run().pet().display_health() #should print 142 and should not print "I am a Dragon"
# dog1.fly() #should not be allowed

#create a Dragon class that inherits Animal attributes/methods, defaults health to 170, fly method increases health by 10, prints "I am a Dragon" when health displayed
class Dragon(Animal):
    def __init__(self, name, health=170):
        super(Dragon, self).__init__(name, health)
    def fly(self):
        self.health += 10
        return self
    def display_health(self):
        super(Dragon, self).display_health()
        print "I am a Dragon!"
        return self
#create a Dragon
dragon1 = Dragon('Gordon')
print dragon1.name
dragon1.walk().run().fly().display_health() #should print 174, plus "I am a Dragon"
# dragon1.pet() #should not be allowed