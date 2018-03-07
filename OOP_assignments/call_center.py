''' OOP Assignment 7: Call Center
You're creating a program for a call center. Every time a call comes in you need a way to track that call. One of your program's requirements is to store calls in a queue while callers wait to speak with a call center employee.

Call Class
Create your call class with an init method. 
    ATTRIBUTES: unique id, caller name, caller phone number, time of call, reason for call
    METHODS: display: that prints all Call attributes.

CallCenter Class
Create your call center class with an init method. 
    ATTRIBUTES: calls: should be a list of call objects;  queue size: should be the length of the call list
    METHODS: add: adds a new call to the end of the call list; remove: removes the call from the beginning of the list (index 0); info: prints the name and phone number for each call in the queue as well as the length of the queue.

Ninja Level: add a method to call center class that can find and remove a call from the queue according to the phone number of the caller.

Hacker Level: If everything is working properly, your queue should be sorted by time, but what if your calls get out of order? Add a method to the call center class that sorts the calls in the queue according to time of call in ascending order. '''

from datetime import datetime, timedelta
class Call(object):
    call_counter = 0  #auto-increment each time a call is created
    now = datetime.strftime(datetime.now(), '%I:%M:%S%p')    
    def __init__(self, caller_name, caller_number, call_reason, call_time=now, call_id=0):
        self.caller_name = caller_name
        self.caller_number = caller_number
        self.call_time = call_time
        self.call_reason = call_reason
        Call.call_counter += 1
        self.call_id = Call.call_counter

    # method to display all call attributes
    def display(self):
        print "Call ID:  {}\nCaller Name:  {}\nPhone Number:  {}\nReason for Calling:  {}\nCall Time:  {}".format(self.call_id, self.caller_name, self.caller_number, self.call_reason, self.call_time)
        return self

class CallCenter(object):
    def __init__(self):
        self.calls = []
        self.calls_queue_size = len(self.calls)
    
    #method to add a call to the queue list
    def add_call(self, call):
        self.calls.append({'id': call.call_id, 'name': call.caller_name, 'number': call.caller_number, 'reason': call.call_reason, 'time': call.call_time})
        self.calls_queue_size = len(self.calls)
        return self
    
    #method to remove the first call(index 0) in the queue list
    def remove_call(self):
        self.calls.pop(0)
        self.calls_queue_size = len(self.calls)
        return self

    # method to display call queue
    def info(self):
        print "="*100
        print "As of {}, remaining calls in queue: {}".format(Call.now, self.calls_queue_size)
        for call in range(len(self.calls)):
            print "Caller: {}, Phone Number: {} Holding since:  {}".format(self.calls[call]['name'], self.calls[call]['number'], self.calls[call]['time'])
        return self
   
    #ninja level - method to remove the a specific all from the queue list based on phone number
    def find_remove(self, phone):
        for call in range(len(self.calls)):
            if self.calls[call]['number'] == phone:
                idx = call  #found the call, break out of loop and remove from queue
                break
        self.calls.pop(idx)
        self.calls_queue_size = len(self.calls)
        return self

    #hacker level - sort the queue list
    def sort_queue(self):
        self.calls.sort(key=lambda x:x['time'])
        return self

#Test Data - Note because timestamp is NOW(), all calls appear to be same time; realistically as calls came in to call center and new calls generated, there would be variation in timestamp. To test, manually input call times, or add randome # of minutes to now
day1 = CallCenter()
call1 = Call("Mike Fowler", "910.555.1212", "WTF? I paid that bill!")
call2 = Call("Shannon Steen", "910.777.1212", "Tech Support")
call3 = Call("Faith Wilson", "910.652.3434", "Complaint-slow drivers")
day1.add_call(call1).add_call(call2).add_call(call3).info()
call4 = Call('JoAnn Benton', "910.452.3333", "Recommendations")
call5 = Call("Laura Sturms", "336.767.1212", "Complaint-missing packages")
day1.remove_call().add_call(call4).add_call(call5).find_remove('910.452.3333').info()
call6 = Call("Jacey Rogers", "910.452.1111", "Complaint-Account Overcharged")
call7 = Call("Charmin Padgett", "910.789.9970", "Billing Payment")
call8 = Call("AJ Rodriguez", "910.664.3590", "Tickets for Game")
day1.add_call(call6).add_call(call7).add_call(call8).remove_call().sort_queue().info()
