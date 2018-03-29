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
    def registration_valid(self, postData):
        errors = {}
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            errors['dup_email'] = "Sorry, that email already exists in the database."
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            errors['fname'] = "Please enter the first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid
            errors['lname'] = "Please enter the last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['password']) < 1 or not PW_REGEX.match(postData['password']): #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if postData['pwconf'] != postData['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        return errors

    #validate login information
    def login_valid(self, postData):
        errors = {}
        try:  
            #search for user based on email address
            user = User.objects.get(email=postData['email'])
            #found one, now confirm password
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()): #passwords do not match
                errors['bad_login'] = "You have entered an invalid email address or password."
        except User.DoesNotExist: #no user found
            errors['bad_login'] = "You have entered an invalid email address or password."
        return errors

    def create_user(self, postData):
        user_count = User.objects.count()
        print user_count
        if user_count == 0:  #no users, register first person as admin
            user_level = 9
        else: #user exist, assign as user
            user_level = 1
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = self.create(first_name=first_name, last_name=last_name, email=email, password=enc_pw, user_level=user_level)
        return user

    def update_user_info(self, postData, user_id):
        errors = {}
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            errors['fname'] = "Please enter the first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid
            errors['lname'] = "Please enter the last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        if len(errors):
            print "we got errors"
            return errors
        print "wonder if we can change the data from here?"
        user = User.objects.get(id=user_id)
        user.first_name = postData['first_name']
        user.last_name = postData['last_name']
        user.email = postData['email']
        user.user_level = postData['user_level']
        user.save()
        return errors  #while there are none, we need to return something so we'll address that in views

    def update_password(self, postData, user_id):
        print "postData from models, {}".format(postData)
        errors = {}
        if len(postData['password']) < 1 or not PW_REGEX.match(postData['password']): #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if postData['pwconf'] != postData['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        if len(errors):
            print "we got errors"
            return errors
        print "wonder if we can change the data from here?"
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = User.objects.get(id=user_id)
        user.password = enc_pw
        user.save
        return errors #while there are none, we need to return something so we'll address that in views

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
