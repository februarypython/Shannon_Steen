from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import MySQLConnector
from datetime import date, datetime
import re # for testing/matching regular expressions
import md5  #imports md5 module to generate a hash (ideally used for passwords)
import os, binascii #import salt feature to make passwords more secure
salt = binascii.b2a_hex(os.urandom(15)) #create the salt string
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num
app = Flask(__name__)
mysql = MySQLConnector(app, 'login_register')
app.secret_key = 'Gmk7Y5PD0G6Ytmyw6FQ87Hhn4jhdKU'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zipcode']
    phone = request.form['mobile']
    
    #validate user input
    errors = False
    if len(first_name) < 2: # not entered, flash error
        flash('Please enter your first name.')
        errors = True
    if len(last_name) < 2: #not entered, flash error
        flash('Please enter your last name')
        errors = True
    if len(email) < 1 or not EMAIL_REGEX.match(email): # not valid
        flash('Please enter a valid email address.')
        errors = True
    if len(password) < 1 or not PW_REGEX.match(password): # not valid
        flash('Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number.', 'bad_pw')
        errors = True
    if request.form['pwconf'] != password: #passwords do not match
        flash('The password you entered does not match. Please try again.', 'pw_conf_fail')
        errors = True
    
    #if there are any errors return user to index.html to correct
    if errors:
        return render_template('index.html', first_name=first_name, last_name=last_name, address=address, city=city, state=state, zip=zip, phone=phone, email=email)   
    else:  #everything is valid, scrub the data, add new record to database, move to success route
        session['status'] = "You have successfully registered."
        hashed_password = md5.new(password + salt).hexdigest() #encrypt password
        mobile = re.sub("\D", "", phone) #scrub phone number

        #add the user
        users_query = "INSERT INTO users VALUES (null, :first_name, :last_name, :email, :password, NOW(), NOW(), :salt)"
        users_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hashed_password,
            'salt': salt
        }
        session['user_id'] = mysql.query_db(users_query, users_data)

        #add the user's address
        address_query = "INSERT INTO addresses VALUES (NULL, :address, :city, :state, :zipcode, NOW(), NOW(), :user_id)"
        address_data = {
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zip,
            'user_id': session['user_id']
        }
        mysql.query_db(address_query, address_data)
        #add the user's mobile number
        phone_query = "INSERT INTO phone_numbers VALUES (NULL, :mobile, NULL, NULL, NULL, NOW(), NOW(), :user_id)"
        phone_data = {
            'mobile': mobile,
            'user_id': session['user_id']
        }
        mysql.query_db(phone_query, phone_data)
        
        #on success move to success page
        return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    #query to find user
    query = "SELECT id, email, password, salt FROM users WHERE email=:email_entered LIMIT 1"
    data = {
        'email_entered': email
    }
    user_found = mysql.query_db(query, data)
    print user_found

    #if user found, verify password entered is correct
    if user_found:
        db_password = user_found[0]['password']
        if db_password == md5.new(password + user_found[0]['salt']).hexdigest(): #if passwords match, log user in
            print "passwords match"
            session['user_id'] = user_found[0]['id'] #save the user_id for subsequent queries
            session['status'] = "You have successfully logged in."
            return redirect('/success')
        else:
            flash("You have entered an invalid email address or password.")
            return redirect('/')    #if user not found, or password is incorrect
    else:
        flash("You have entered an invalid email address or password.")
        return redirect('/')

@app.route('/success')
def success():
    #query user details
    query = "SELECT first_name, last_name, email, address, city, state, zipcode, mobile, work, work_ext, other FROM users LEFT JOIN addresses ON addresses.user_id = users.id LEFT JOIN phone_numbers ON phone_numbers.user_id = users.id WHERE users.id = :id"
    data = {
        'id': session['user_id']
    }
    result = mysql.query_db(query, data)
    return render_template('account.html', result=result)

@app.route('/update', methods=['POST'])
def update():
    email = request.form['email']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zipcode']
    mobile = request.form['mobile']
    work = request.form['work']
    ext = request.form['work_ext']
    other = request.form['other']
    #validate user input
    if len(email) < 1 or not EMAIL_REGEX.match(email): # not valid
        flash('Please enter a valid email address.')
        return redirect('/success')
    else:
        # update database with new address
        address_query = "UPDATE addresses SET address=:address, city=:city, state=:state, zipcode=:zip, updated_at=NOW() WHERE user_id=:id"
        address_data = {
            'address': address,
            'city': city,
            'state': state,
            'zip': zip,
            'id': session['user_id']
        }
        mysql.query_db(address_query, address_data)
        #update database with new phone number(s)
        mobile = re.sub("\D", "", mobile) #scrub the mobile number
        work = re.sub("\D", "", work) #scrub the work number number
        other = re.sub("\D", "", other) #scrub the other number
        phone_query = "UPDATE phone_numbers SET mobile=:mobile, work=:work, work_ext=:ext, other=:other, updated_at=NOW() WHERE user_id=:id"
        phone_data = {
            'mobile': mobile,
            'work': work,
            'ext': ext,
            'other': other,
            'id': session['user_id']
        }
        mysql.query_db(phone_query, phone_data)
        #update database with new email address
        user_query = "UPDATE users SET email=:email, updated_at:=NOW() WHERE id=:id"
        user_data = {
            'email': email,
            'id': session['user_id']
        }
        mysql.query_db(user_query, user_data)
        session['status'] = "Your information has been updated."
        return redirect('/success')

app.run(debug=True)