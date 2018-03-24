# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import connection
import bcrypt #for enctypting passwords
import re #for testing/matching regular expressions
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #regex for proper email format
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num

# Create your models here.
class UserManager(models.Manager):
    #validate registration information
    def registration_valid(self, postData):
        print "postData from models, {}".format(postData)
        errors = {}
        if not NAME_REGEX.match(postData['name']):  #null or invalid
            errors['name'] = "Please enter your full name (first and last), ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['alias']):  #null or invalid      
            errors['alias'] = "Please enter your alias or nickname, ensuring invalid characters (numbers, symbols) are not included."
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']): #null or invalid
            errors['email'] = "Please enter a valid email address."
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            errors['dup_email'] = "Sorry, that email already exists in the database."
        if len(postData['password']) < 1 or not PW_REGEX.match(postData['password']): #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if postData['pwconf'] != postData['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        print "errors from models, {}".format(errors)
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
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = self.create(name=name, alias=alias, email=email, password=enc_pw)
        return user

class BookManager(models.Manager):
    #validations here
    def newbook_valid(self, postData):
        errors = {}
        #check if book is already in database
        if len(postData['title']) < 1: #null
            errors['title'] = "Please enter the Title of the book you'd like to add."
        if Book.objects.filter(title=postData['title']): #book already in db
            errors['dup_book'] = "That book already exists in the database. Perhaps you'd like to review it?"
        if postData['author'] == "select from the list" and len(postData['author_new']) < 1: #author not selected or entered
            errors['author'] = "Please enter the Author of the book. You have to option to select from the list or, if not there, add add a new one."            
        if len(postData['review']) < 1: #null
            errors['review'] = "Since this is book is new to our collection of book reviews, we'd really like your opinion. Please add a review now."
        if postData['rating'] < 1: #no rating entered
            errors['rating'] = "Since this is book is new to our collection of book reviews, we'd really like your opinion. Please rate the book now."
        return errors
    
    def create_book(self, postData, reviewer_id):
        #create the author first
        if postData['author'] != "select from the list": #user chose one from database, do not create new
            this_author = Author.objects.get(id=postData['author'])  #get will work as there should only be one
        else: #user trying to add new author
            try:  
                #search for author in db, if exists do not create
                this_author = Author.objects.get(author_name=postData['author_new'])
                #found one, do not create new
                pass
            except Author.DoesNotExist: #no author found, create new one
                author = postData['author_new']
                this_author = Author.objects.create(author_name=author)
        
        #create the book, with author attached
        title = postData['title']
        new_book = self.create(title=title, author=this_author)

        #create the review, with book and user attached
        review = postData['review']
        rating = postData['rating']
        reviewer = User.objects.get(id=reviewer_id)
        new_review = Review.objects.create(review=review, rating=rating, reviewer=reviewer, book=new_book)
        print new_book, new_review
        return new_book

    def valid_review(self, postData):
        errors = {}
        if len(postData['review']) < 1: #null
            errors['review'] = "Hey, your forgot to add your review. Please add it now."
        if postData['rating'] < 1: #no rating entered
            errors['rating'] = "If you don't mind terribly, please go ahead and rate the book now."
        return errors

    def add_review(self, book_id, reviewer_id, postData):
        review = postData['review']
        rating = postData['rating']
        book = Book.objects.get(id=book_id)
        reviewer = User.objects.get(id=reviewer_id)
        new_review = Review.objects.create(review=review, rating=rating, reviewer=reviewer, book=book)
        return new_review

    def get_all_books(self):
        all_books = []
        books = Book.objects.all()
        for book in books:
            print book.id, book.title
            all_books.append({'book_id': book.id, 'title': book.title, 'author': book.author})
            print all_books

    # def get_all_books(self):
    #     books = Book.objects.raw("SELECT books_book.id AS 'book_id', books_book.title AS 'title', books_author.author_name AS 'author', books_review.review AS 'review', books_review.rating AS 'rating', books_user.id AS 'reviewer_id', books_user.alias AS 'reviewer', books_review.created_at AS 'reviewed' FROM books_book LEFT JOIN books_review ON books_review.book_id = books_book.id LEFT JOIN books_user ON books_review.reviewer_id = books_user.id LEFT JOIN books_author on books_author.id = books_book.author_id ORDER BY reviewed")
    #     return books
    #     # return books


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of UserManager overwriting old objects key with new properties
    objects = UserManager()

    def __str__(self):
	    return 'User Info: %s %s %s' % (self.name, self.alias, self.email)

class Author(models.Model):
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return '%s' % (self.author_name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of BookManager overwriting old objects key with new properties
    objects = BookManager()

    def __str__(self):
	    return 'Book Info: %s %s' % (self.title, self.author)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()  #validate # between 1-5
    reviewer = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Review Info:  %s written by %s on book %s' % (self.review, self.reviewer, self.book)