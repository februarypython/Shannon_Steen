from flask import Flask, render_template
app = Flask(__name__)
@app.route('/') #default home page (index.html)
def index():
    return render_template('index.html')
@app.route('/projects') #route to projects.html page
def projects():
    return render_template('projects.html')
@app.route('/about') #route to about.html page
def about():
    return render_template('about.html')
app.run(debug=True)