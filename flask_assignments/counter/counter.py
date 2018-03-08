from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "MySecretKey"
@app.route('/')
def index():
    if 'counter' not in session:  #initialize counter to 1 for first view
        session['counter'] = 1
    else:
        session['counter'] += 1  #add 1 to counter for subsequent views when page is reloaded
    return render_template('index.html')
@app.route('/add2')
def add2():
    session['counter'] += 2
    return render_template('index.html')
@app.route('/reset')
def reset():
    session['counter'] = 0
    return redirect('/')
app.run(debug=True)