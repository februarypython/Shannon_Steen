''' OOP Assignment 6 - MathDojo
PART I
Create a Python class called MathDojo that has the methods add and subtract. Have these 2 functions take at least 1 parameter.

Then create a new instance called md. It should be able to do the following task:
md.add(2).add(2,5).subtract(3,2).result
which should perform 0+2+(2+5)-(3+2) and return 4.

PART II
Modify MathDojo to take at least one integer(s) and/or list(s) as a parameter with any number of values passed into the list. It should now be able to perform the following tasks:

md.add([1], 3,4).add([3,5,7,8], [2,4.3,1.25]).subtract(2, [2,3], [1.1,2.3]).result
should do 0+1+3+4+(3+5+7+8)+(2+4.3+1.25)-2-(2+3)-(1.1+2.3) and return its result of 28.15.

PART III
Make any needed changes in MathDojo in order to support tuples of values in addition to lists and singletons. '''

class MathDojo(object):
    def __init__(self):
        self.result = 0
    
    def add(self, *args):
        if not args:
            print "Please provide numbers to perform math calculations"
        else:
            for arg in args: #evaluate arg input and do math
                if type(arg) == str or type(arg) == dict:  #fast fail
                    print "Please provide numbers to perform math calculations"
                    return self
                elif type(arg) == list: #dealing with list
                    argsum = 0 
                    for idx in range(len(arg)):
                        if type(arg[idx]) == str or type(arg[idx]) == dict: #fast fail
                            print "Please provide numbers to perform math calculations"
                            return self
                        else:
                            argsum += arg[idx] #do the math on values in list
                    arg = argsum #arg is now the sum of all values in list
                elif type(arg) == tuple: #dealing with tuple
                    argsum = 0 
                    for val in arg:
                        if type(val) == str or type(val) == dict: #fast fail
                            print "Please provide numbers to perform math calculations"
                            return self
                        else:
                            argsum += val #do the math on values in tuples
                    arg = argsum #arg is now the sum ov all values in tuple
                self.result += arg
        return self

    def subtract(self, *args):
        if not args:
            print "Please provide numbers to perform math calculations"
            return self
        else:
            for arg in args: #evaluate arg input and do math
                if type(arg) == str or type(arg) == dict:  #fast fail
                    print "Please provide numbers to perform math calculations"
                    return self
                elif type(arg) == list: #dealing with list
                    argsum = 0 
                    for idx in range(len(arg)):
                        if type(arg[idx]) == str or type(arg[idx]) == dict: #fast fail
                            print "Please provide numbers to perform math calculations"
                            return self
                        else:
                            argsum += arg[idx] #do the math on values in list
                    arg = argsum #arg is now the sum of all values in list
                elif type(arg) == tuple: #dealing with tuple
                    argsum = 0 
                    for val in arg:
                        if type(val) == str or type(val) == dict: #fast fail
                            print "Please provide numbers to perform math calculations"
                            return self
                        else:
                            argsum += val #do the math on values in tuples
                    arg = argsum #arg is now the sum ov all values in tuple
                self.result -= arg
        return self



md = MathDojo()
# print md.add(2).add(2,5).subtract(3,2).result  #returns 4
# print md.add([1], 3,4).add([3,5,7,8], [2,4.3,1.25]).subtract(2, [2,3], [1.1,2.3]).result  #returns 28.15