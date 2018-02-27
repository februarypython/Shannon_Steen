from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import MySQLConnector
import re #for validating email address
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'Id0n0tLVpi'
mysql = MySQLConnector(app, 'emailsdb')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form['email']
    session['email'] = email
    # check to see if email is valid
    if len(email) < 1 or not EMAIL_REGEX.match(email): #email not entered or not valid format
        flash('Please enter a valid email address.')
        return redirect('/')
    else:
        query = "SELECT email FROM emails WHERE email=:email_to_check"
        data = {'email_to_check':email}
        email_check = mysql.query_db(query, data)
        #check to see if email is in database already
        if (email_check):  #found a match in database
            return redirect('/success')
        else: #add new email to database
            query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
            data = {'email': email}
            mysql.query_db(query, data) #run the query
            return redirect('/success')

@app.route('/success')
def success():
#peform new query to return all database emails
    query = "SELECT email, DATE_FORMAT(created_at, '%M %e, %Y %h:%i%p') AS 'date' FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails=emails, email=session['email'])
app.run(debug=True)