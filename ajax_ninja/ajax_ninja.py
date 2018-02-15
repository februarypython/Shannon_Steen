from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/red')
def red_turtle():
    red_turtle = {
        'name': 'Raphael',
        'color': 'red',
        'weapons': 'twin sai',
        'attitude': ['aggressive', 'rebellious', 'angry'],
        'brother_position': '2nd eldest'
    }
    resp = jsonify(red_turtle)
    resp.headers['Access-Control-Allow-Origin']="*" # to allow for testing
    return resp

@app.route('/blue')
def blue_turtle():
    blue_turtle = {
        'name': 'Leonardo',
        'color': 'blue',
        'weapons': 'two katanas',
        'attitude': ['spiritual', 'disciplined', 'serious'],
        'brother_position': 'eldest'
    }
    resp = jsonify(blue_turtle)
    resp.headers['Access-Control-Allow-Origin']="*" # to allow for testing
    return resp

@app.route('/orange')
def orange_turtle():
    orange_turtle = {
        'name': 'Michelangelo',
        'color': 'orange',
        'weapons': 'dual nunchaku',
        'attitude': ['fun-loving', 'carefree', 'playful'],
        'brother_position': 'youngest'
    }
    resp = jsonify(orange_turtle)
    resp.headers['Access-Control-Allow-Origin']="*" # to allow for testing
    return resp

@app.route('/purple')
def purple_turtle():
    purple_turtle = {
        'name': 'Donatello',
        'color': 'purple',
        'weapons': 'a bo staff',
        'attitude': ['smart', 'calm', 'tech savvy'],
        'brother_position': '2nd youngest'
    }
    resp = jsonify(purple_turtle)
    resp.headers['Access-Control-Allow-Origin']="*" # to allow for testing
    return resp

@app.route('/other')
def other_turtle():
    other_turtle = {
        'name': 'April O\'Neil',
        'color': 'yellow',
        'weapons': 'a camcorder',
        'attitude': ['independent', 'driven', 'loyal'],
        'brother_position': 'news reporter'
    }
    resp = jsonify(other_turtle)
    resp.headers['Access-Control-Allow-Origin']="*" # to allow for testing
    return resp

app.run(debug=True)