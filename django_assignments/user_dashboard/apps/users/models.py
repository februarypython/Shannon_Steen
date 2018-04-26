# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt #for enctypting passwords
import re #for testing/matching regular expressions
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #regex for proper email format
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num

# Create your models here.
class UserManager(models.Manager):
    #validate registration information
    def registration_valid(self, post_data):
        errors = {}
        if len(post_data['email']) < 1 or not EMAIL_REGEX.match(post_data['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        #check if email is already in database
        if User.objects.filter(email=post_data['email']): #email already in db
            errors['dup_email'] = "Sorry, that email already exists in the database."
        if not NAME_REGEX.match(post_data['first_name']):  #null or invalid
            errors['fname'] = "Please enter the first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(post_data['last_name']):  #null or invalid
            errors['lname'] = "Please enter the last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(post_data['password']) < 1 or not PW_REGEX.match(post_data['password']): #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if post_data['pwconf'] != post_data['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        return errors

    #validate login information
    def login_valid(self, post_data):
        errors = {}
        try:  
            #search for user based on email address
            user = User.objects.get(email=post_data['email'])
            #found one, now confirm password
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()): #passwords do not match
                errors['bad_login'] = "You have entered an invalid email address or password."
        except User.DoesNotExist: #no user found
            errors['bad_login'] = "You have entered an invalid email address or password."
        return errors

    def create_user(self, post_data):
        user_count = User.objects.count()
        print user_count
        if user_count == 0:  #no users, register first person as admin
            user_level = 9
        else: #users exist, assign as user
            user_level = 1
        first_name = post_data['first_name']
        last_name = post_data['last_name']
        email = post_data['email']
        enc_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = self.create(first_name=first_name, last_name=last_name, email=email, password=enc_pw, user_level=user_level)
        return user

    def update_user_info(self, post_data, user_id):
        errors = {}
        if not NAME_REGEX.match(post_data['first_name']):  #null or invalid
            errors['fname'] = "Please enter the first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(post_data['last_name']):  #null or invalid
            errors['lname'] = "Please enter the last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(post_data['email']) < 1 or not EMAIL_REGEX.match(post_data['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        if errors:
            return errors
        user = User.objects.get(id=user_id)
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.email = post_data['email']
        user.user_level = post_data['user_level']
        user.save()
        return user

    def update_password(self, post_data, user_id):
        print "post_data from models, {}".format(post_data)
        errors = {}
        if len(post_data['password']) < 1 or not PW_REGEX.match(post_data['password']): #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if post_data['pwconf'] != post_data['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        if errors:
            return errors
        enc_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = User.objects.get(id=user_id)
        user.password = enc_pw
        user.save
        return user
    
    def update_user_desc(self, post_data, user_id):
        #no need to validate, make the changes
        user = User.objects.get(id=user_id)
        user.description = request.POST['desc']
        user.save()
        return user

class User(models.Model):
    STATUS_CHOICES = (
        (1, 'normal'),
        (9, 'admin'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField(choices=STATUS_CHOICES, default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of UserManager overwriting old objects key with new properties
    objects = UserManager()

    def __str__(self):
	    return 'User Info: %s %s %s' % (self.first_name, self.last_name, self.user_level)
