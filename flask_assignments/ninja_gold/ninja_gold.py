from flask import Flask, render_template, request, redirect, session
import random
import time
from time import localtime, strftime
app = Flask(__name__)
app.secret_key = 'myTopSecretKey' #you need to set a secret key for security purposes
@app.route('/')
def index():
    if 'ninja_gold' not in session: #first visit, initialize ninja_gold
        session['ninja_gold'] = 0
    else:
        session['ninja_gold'] = session['ninja_gold'] #return visit, carry win activities forward
    if 'ninja_wins' not in session: #first visit, initializze ninja_wins
        session['ninja_wins'] = []
    else:
        session['ninja_wins'] = session['ninja_wins']
    if 'ninja_losses' not in session: #first visit, initializze ninja_losses
        session['ninja_losses'] = []
    else:
        session['ninja_losses'] = session['ninja_losses']
    return render_template('index.html', gold=session['ninja_gold'], wins=session['ninja_wins'], losses=session['ninja_losses'])

@app.route('/process_gold', methods=['POST'])
def process_gold():
    print "gold so far"
    print session['ninja_gold']
    time = strftime("%a, %b %d, %I:%M %p", localtime())
    print time
    if request.form['building'] == 'farm':  #user went to the farm
        print "user went to the farm"
        session['farm_gold'] = random.randint(10, 20) #credit random about between 10-20
        print "farm gold won"
        print session['farm_gold']
        session['ninja_gold'] += session['farm_gold']
        session['ninja_wins'].append("Earned "+str(session['farm_gold'])+" golds from the farm! "+str(time))
        print session['ninja_wins'] 
    elif request.form['building'] == 'cave':  #user went to the cave
        print "user went to the cave"
        session['cave_gold'] = random.randint(5, 10) #credit random about between 5-10
        print "cave gold won"
        print session['cave_gold']
        session['ninja_wins'].append("Earned "+str(session['cave_gold'])+" golds from the cave! "+str(time))
        print session['ninja_wins'] 
        session['ninja_gold'] += session['cave_gold']
    elif request.form['building'] == 'house':  #user went to the house
        print "user went to the house"
        session['house_gold'] = random.randint(2, 5) #credit random about between 2-5
        print "house gold won"
        print session['house_gold']
        session['ninja_gold'] += session['house_gold']
        session['ninja_wins'].append("Earned "+str(session['house_gold'])+" golds from the house! "+str(time))
        print session['ninja_wins'] 
    else:   #user went to the casino
        print "user went to the casino"
        session['casino_gold'] = random.randint(-50, 50) #credit/debit random about between -50 to 50
        print "casino gold won/loss"
        print session['casino_gold']
        session['ninja_gold'] += session['casino_gold']
        if session['casino_gold'] < 0:  #lost money in casino
            session['ninja_losses'].append("Entered a casino and lost "+str(session['casino_gold'])+" golds. Ouch! "+str(time))
        else: #won money in casino
            session['ninja_wins'].append("Entered a casino and won "+str(session['casino_gold'])+" golds. Sweet! "+str(time))
        print session['ninja_wins'] 
        print session['ninja_losses'] 
    return redirect('/')
app.run(debug=True)