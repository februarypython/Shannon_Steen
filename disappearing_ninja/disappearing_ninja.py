from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ninja')
def ninja():
    return render_template('ninja.html')
@app.route('/ninja/<input>')
def show_turtle(input):
    if input == "blue" or input == "leonardo":
        return render_template('ninja_blue.html')
    elif input == "orange" or input == "michelangelo":
        return render_template('ninja_orange.html')
    elif input == "red" or input == "raphael":
        return render_template('ninja_red.html')
    elif input == "purple" or input == "donatello":
        return render_template('ninja_purple.html')
    else:
        return render_template('ninja_other.html')
app.run(debug=True)