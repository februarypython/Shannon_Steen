# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re # for testing/matching regular expressions
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #reget to confirm email address valid
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            print "no name entered"
            errors['first_name'] = "Please enter your first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid      
            print "no name entered"
            errors['last_name'] = "Please enter your last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            print "no email entered"
            errors['email'] = "Please enter a valid email address."
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            print "email already exists"
            errors['dup_email'] = "Sorry, that email already exists in the database."
        return errors

    def create_user(self, fname, lname, email):
        user = self.create(first_name=fname, last_name=lname, email=email)
        return user
    
    def validate_changes(self, postData):
        errors = {}
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            print "no name entered"
            errors['first_name'] = "Please enter your first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid      
            print "no name entered"
            errors['last_name'] = "Please enter your last name, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            print "no email entered"
            errors['email'] = "Please enter a valid email address."
        return errors   

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of UserManager overwriting old objects key with new properties
    objects = UserManager()

    def __str__(self):
		return 'User Info: %s %s %s' % (self.first_name, self.last_name, self.email)
