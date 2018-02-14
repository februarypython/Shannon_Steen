from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "thisIsSecret"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/color', methods=['POST'])
def get_color():
    session['red'] = request.form['red']
    session['green'] = request.form['green']
    session['blue'] = request.form['blue']
    return render_template('index.html', redNo=session['red'], greenNo=session['green'], blueNo=session['blue'])
app.run(debug=True)