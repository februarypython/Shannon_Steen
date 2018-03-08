from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import MySQLConnector
import re # for testing/matching regular expressions
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #reget to confirm email address valid
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters

app = Flask(__name__)
mysql = MySQLConnector(app, 'full_friends')
app.secret_key = 'Gmk7Y5PD0G6Ytmyw6FQ87Hhn4jhdKU'

@app.route('/')
def login():
    return redirect('/users')

#show all users
@app.route('/users')
def index():
    #query for all users
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS 'name', email, DATE_FORMAT(created_at, '%M %e, %Y') AS 'created' FROM friends"
    users = mysql.query_db(query)
    return render_template('index.html', users=users)

#display form for adding new user
@app.route('/users/new')
def new():
    if 'first_name' not in session:
        session['first_name'] = ""
    if 'last_name' not in session:
        session['last_name'] = ""    
    if 'email' not in session:
        session['email'] = ""
    return render_template('new.html', first_name=session['first_name'], last_name=session['last_name'], email=session['email'])

#create the new user
@app.route('/users/create', methods=['POST'])
def create():
    errors = False
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    #validate user input
    if not NAME_REGEX.match(session['first_name']): # null or invalid, flash error
        print "no name entered"
        flash('Please enter your first name, ensuring invalid characters (numbers, symbols) are not included.')
        errors = True
    if not NAME_REGEX.match(session['last_name']): #null or invalid, flash error
        flash('Please enter your last name, ensuring invalid characters (numbers, symbols) are not included.')
        errors = True
    #check if email is already in database
    email_query = "SELECT id FROM friends WHERE email=:email_entered"
    email_data = {'email_entered': session['email']}
    if mysql.query_db(email_query, email_data):
        flash("Sorry, that email already exists in the database.")
        errors = True
    if len(session['email']) < 1 or not EMAIL_REGEX.match(session['email']): # not valid
        flash('Please enter a valid email address.')
        errors = True
    
    #if there are any errors return user to new.html to correct
    if errors:
        return redirect(url_for('new'))   
    else:  #everything is valid, add new user to the database
        create_query = "INSERT INTO friends VALUES(NULL, :first, :last, NULL, NOW(), NOW(), :email)"
        create_data = {
                'first': request.form['first_name'],
                'last': request.form['last_name'],
                'email': request.form['email']
        }
        #save the new user id number, pass to show_user to display new user
        new_id = mysql.query_db(create_query, create_data)
        return redirect(url_for('show', id=new_id))

#show a specific user
@app.route('/users/<id>')
def show(id):
    #query for single user
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS 'name', email, DATE_FORMAT(created_at, '%M %e, %Y') AS 'created' FROM friends WHERE id=:user_id"
    data = {'user_id': id}
    user = mysql.query_db(query, data)
    return render_template('show.html', user=user[0])

#on GET, display form to edit specific user
@app.route('/users/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    #query for single user
    query = "SELECT id, first_name, last_name, email FROM friends WHERE id=:user_id"
    data = {'user_id': id}
    user = mysql.query_db(query, data)
    return render_template('edit.html', user=user[0])

#on POST, update the specifc user and return to show
@app.route('/users/<id>', methods=['POST'])
def update(id):
    # if request.method == 'POST':
    print "making updates to user"
    #make the change to the database
    edit_query = "UPDATE friends SET first_name=:first, last_name=:last, email=:email, updated_at=NOW() WHERE id=:user_id"
    edit_data = {
        'first': request.form['first_name'],
        'last': request.form['last_name'],
        'email': request.form['email'],
        'user_id': id
    }
    mysql.query_db(edit_query, edit_data)
    return redirect(url_for('show', id=id))

@app.route('/users/<id>/destroy')
def destroy(id):
    #delete the user
    delete_query = "DELETE FROM friends WHERE id=:user_id"
    delete_data = {'user_id': id}
    mysql.query_db(delete_query, delete_data)
    return redirect(url_for('index'))


@app.route('/signout')
def signout():
    session.pop('user_id', 'first_name')
    return redirect('/')

app.run(debug=True)