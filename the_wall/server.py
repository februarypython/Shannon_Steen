from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import MySQLConnector
from datetime import date, datetime, timedelta
import re # for testing/matching regular expressions
import md5  #imports md5 module to generate a hash (ideally used for passwords)
import os, binascii #import salt feature to make passwords more secure
salt = binascii.b2a_hex(os.urandom(15)) #create the salt string
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num
app = Flask(__name__)
mysql = MySQLConnector(app, 'the_wall')
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
    
    #validate user input
    errors = False
    if not NAME_REGEX.match(first_name): # null or invalid, flash error
        flash('Please enter your first name, ensuring invalid characters (numbers, symbols) are not included.')
        errors = True
    if not NAME_REGEX.match(last_name): #null or invalid, flash error
        flash('Please enter your last name, ensuring invalid characters (numbers, symbols) are not included.')
        errors = True
    #check if email is already in database
    email_query = "SELECT id FROM users WHERE email=:email_entered"
    email_data = {'email_entered': email}
    if mysql.query_db(email_query, email_data):
        flash("Sorry, that email already exists in the database.")
        errors = True
    if len(email) < 1 or not EMAIL_REGEX.match(email): # not valid
        flash('Please enter a valid email address.')
        errors = True
    if len(password) < 1 or not PW_REGEX.match(password): # not valid
        flash('Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number.')
        errors = True
    if request.form['pwconf'] != password: #passwords do not match
        flash('The password you entered does not match. Please try again.')
        errors = True
    
    #if there are any errors return user to index.html to correct
    if errors:
        return render_template('index.html', first_name=first_name, last_name=last_name, email=email)   
    else:  #everything is valid, scrub the data, add new user to database, move to the wall route
        hashed_password = md5.new(password + salt).hexdigest() #encrypt password

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
        return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    #query to find user
    query = "SELECT id, first_name, email, password, salt FROM users WHERE email=:email_entered LIMIT 1"
    data = {
        'email_entered': email
    }
    user_found = mysql.query_db(query, data)

    #if user found, verify password entered is correct
    if user_found:
        if user_found[0]['password'] == md5.new(password + user_found[0]['salt']).hexdigest(): #if passwords match, log user in
            print "passwords match"
            session['user_id'] = user_found[0]['id'] #save the user_id for subsequent queries
            session['first_name'] = user_found[0]['first_name']
            return redirect('/wall')
        else:
            flash("You have entered an invalid email address or password.")
            return redirect('/')    #if user not found, or password is incorrect
    else:
        flash("You have entered an invalid email address or password.")
        return redirect('/')

@app.route('/wall')
def wall():
    #if user not in session, redirect
    if 'user_id' not in session:
        return redirect('/')
    else: #user logged in, personalize page
        user_query = "SELECT first_name FROM users WHERE id=:logged_id"
        user_data = {'logged_id': session['user_id']}
        user=mysql.query_db(user_query, user_data)

        #query posts(aka messages)
        post_query = "SELECT CONCAT_WS(' ', first_name, last_name) AS 'poster', messages.user_id AS 'poster_id', message AS 'post', DATE_FORMAT(messages.created_at, '%M %e, %Y') AS 'posted', messages.id AS 'msgid', messages.created_at FROM users JOIN messages ON messages.user_id=users.id ORDER BY DATE_FORMAT(messages.created_at, '%M %e, %Y') DESC"
        posts = mysql.query_db(post_query)
        #loop through each post and query for any comments
        comment_query = "SELECT CONCAT_WS(' ', first_name, last_name) AS 'commenter', comment, DATE_FORMAT(comments.created_at, '%M %e, %Y') AS 'commented', message_id from comments JOIN users on users.id=comments.user_id ORDER BY DATE_FORMAT(comments.created_at, '%M %e, %Y')"
        comments = mysql.query_db(comment_query)

        now = datetime.now()
        return render_template('wall.html', user=session['first_name'], posts=posts, comments=comments, now=now)

@app.route('/message', methods=['POST'])
def message():
    #if user not in session, redirect
    if 'user_id' not in session:
        return redirect('/')
    else:
        post_query = "INSERT INTO messages VALUES (NULL, :id, :post, NOW(), NOW())"
        post_data = {
            'id': session['user_id'],
            'post': request.form['post']
        }
        mysql.query_db(post_query, post_data)
        return redirect('/wall')

@app.route('/comment', methods=['POST'])
def comment():
    #if user not in session, redirect
    if 'user_id' not in session:
        return redirect('/')
    else:
        comment_query = "INSERT INTO comments VALUES (NULL, :userid, :msgid, :post, NOW(), NOW())"
        comment_data = {
            'userid': session['user_id'],
            'msgid': request.form['msgid'],
            'post': request.form['comment']
        }
        mysql.query_db(comment_query, comment_data)
        return redirect('/wall')

@app.route('/delete/<msgid>')
def delete_post(msgid):
    #if user not in session, redirect
    if 'user_id' not in session:
        return redirect('/')
    else:
        #find any comments tied to message and delete them
        comments_query = "SELECT id from comments WHERE message_id=:msgid"
        comments_data = {'msgid': msgid}
        comments_del = mysql.query_db(comments_query, comments_data)
        for comment in comments_del:
            comment_del_query = "DELETE FROM comments WHERE id=:cmtid"
            comment_del_data = {'cmtid': comment['id']}
            mysql.query_db(comment_del_query, comment_del_data)
        #now delete the message
        post_del_query = "DELETE FROM messages WHERE id=:msgid"
        post_del_data = {'msgid': msgid}
        mysql.query_db(post_del_query, post_del_data)
        return redirect('/wall')
        # del_query = "DELETE FROM comments"


@app.route('/signout')
def signout():
    session.pop('user_id', 'first_name')
    return redirect('/')

app.run(debug=True)