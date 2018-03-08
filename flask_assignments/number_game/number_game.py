from flask import Flask, render_template, request, url_for, session, redirect
import random
app = Flask(__name__)
app.secret_key = 'myTopSecretKey' #you need to set a secret key for security purposes
@app.route('/')
def index():
    session['rand_no'] = random.randint(1, 100) #generate random number between 1-100
    print "the random num initialized is "
    print session['rand_no']

    if 'comp_wins' not in session: #let's keep track of how many times computer wins
        session['comp_wins'] = 0 #haven't played before
    else:
        session['comp_wins'] += 1 #computer won
    if 'user_wins' not in session: #let's keep track of how many times user wins
        session['user_wins'] = 0 #haven't played before; wins credit under correct route

    return render_template("index.html", random=session['rand_no'], comp_wins=session['comp_wins'], user_wins=session['user_wins']) #pass the number and win/loss stats

@app.route('/result', methods=['POST'])
def result():
    session['guess'] = int(request.form['guess']) #convert response to a number
    print "the user guessed "
    print session['guess']

    return render_template("result.html", guess=session['guess'], random=session['rand_no'], comp_wins=session['comp_wins'], user_wins=session['user_wins']) #pass the guess, the number, and the win/loss stats

@app.route('/correct', methods=['POST'])
def correct():
    session['user_wins'] += 1 #user won
    session.pop('guess')    #reset the values
    session.pop('rand_no')  #reset the values
    return redirect('/')    #start again

app.run(debug=True)