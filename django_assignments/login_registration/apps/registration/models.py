# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
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
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            errors['first_name'] = "Please enter your first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid      
            errors['last_name'] = "Please enter your last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['birthdate']) < 1:  #null
            errors['birthdate'] = "Please enter your date of birth."
        else:
            #verify user is at least 12 yrs old (and not older than 120)
            dob = datetime.strptime(postData['birthdate'], "%Y-%m-%d").date()
            today = datetime.now().date()
            age = (today - dob).days
            age = age/365
            if age < 12:
                errors['birthdate'] = "You must be at least 12 years of age to register."
            elif age > 120:
                errors['birthdate'] = "If you really are {} years old, please contact the Guinness Book of World records. Otherwise, Please enter a valid birthdate.".format(age)
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            errors['dup_email'] = "Sorry, that email already exists in the database."
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
        fname = postData['first_name']
        lname = postData['last_name']
        email = postData['email']
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())  #encrypt password
        dob = postData['birthdate']
        user = self.create(first_name=fname, last_name=lname, email=email, password=enc_pw, birthdate=dob)
        return user

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of UserManager overwriting old objects key with new properties
    objects = UserManager()

    def __str__(self):
	    return 'User Info: %s %s %s' % (self.first_name, self.last_name, self.email)
