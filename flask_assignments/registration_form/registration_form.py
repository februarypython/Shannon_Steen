from flask import Flask, render_template, request, redirect, session, flash, url_for
import re # for testing/matching regular expressions
from datetime import date, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num
app = Flask(__name__)
app.secret_key = 'Id0n0tLVpi'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def validate():
    # establish data variables to return if validation fails
    resp = ""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    pword = request.form['password']
    birthdate = request.form['birth_date']
    #convert birthdate to date object for comparison
    if birthdate:     
        dob = datetime.strptime(birthdate, '%Y-%m-%d').date() 
    
    #now do some validations
    if len(first_name) < 1:
 	    resp = "failed firstname"
    elif len(last_name) < 1:
 	    resp = "failed lastname"
    elif len(email) < 1 or not EMAIL_REGEX.match(email):
 	    resp = "failed email"
    elif len(pword) < 1 or not PW_REGEX.match(pword):
 	    resp = "failed password"
    elif request.form['password_conf'] != pword:
  	    resp = "failed password conf"
    elif bool(birthdate) == False or dob > date.today():
	    resp = "failed birthdate"
    else:
	    resp = "success"
    #pass result of validation testing for final processing
    return(result(resp))

#final check to determine what, if any, errors to show and page to render
def result(result):  
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    pword = request.form['password']
    birthdate = request.form['birth_date']

    if result == "success":
        return render_template('registered.html')
    else:
        if result == "failed firstname":
            flash('Please enter your first name.', 'blank_first_name')
        if result == "failed lastname":
            flash('Please enter your last name.', 'blank_last_name')
        if result == "failed email":
            flash('Please enter a valid email address.', 'bad_email')
        if result == "failed password":
            flash('Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number.', 'bad_pw')
        if result == "failed password conf":
            flash('The password you entered does not match. Please try again.', 'pw_conf_fail')
        if result == "failed birthdate":
            flash('Please enter your date of birth.', 'bad_dob')
    return render_template('index.html', firstname=first_name, lastname=last_name, email=email, password=pword, birth_date=birthdate)

app.run(debug=True)