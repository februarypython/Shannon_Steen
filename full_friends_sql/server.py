from flask import Flask, render_template, redirect, request, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'full_friends')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = "SELECT CONCAT_WS(' ', first_name, last_name) AS 'name', age, DATE_FORMAT(created_at, '%M %D') AS 'since', DATE_FORMAT(created_at, '%Y') as 'year' FROM friends"
        friends = mysql.query_db(query)
        return render_template('index.html', all_friends=friends)
    else:  #user is adding a friend, save friend to database
        query = "INSERT INTO friends VALUES (null, :first_name, :last_name, :age, NOW(), NOW())"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'age': request.form['age'],
        }
        mysql.query_db(query, data)
        return redirect('/')
app.run(debug=True)