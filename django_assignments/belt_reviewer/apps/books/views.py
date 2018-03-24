# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages  #for flashing error messages
from django.db.models import Count
from django.contrib.auth import authenticate, login
from .models import User, Author, Book, Review

# Create your views here.

#show home page
def index(request):
    return render(request, 'books/index.html')

#create new user
def register(request):
    print "request.POST from views, {}".format(request.POST)
    request.session['newusername'] = request.POST['name']
    request.session['newuseralias'] = request.POST['alias']
    request.session['newuseremail'] = request.POST['email']
    #validate data
    errors = User.objects.registration_valid(request.POST)
    print "errors from views, {}".format(errors)
    if len(errors): #if there are any errors return user to homepage to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('homepage'))
    else: #add new user
        user = User.objects.create_user(request.POST)
        request.session['user_id'] = user.id
        request.session['alias'] = user.alias
        return redirect(reverse('book_index'))

#login existing user
def login(request):
    #validate login
    errors = User.objects.login_valid(request.POST)
    if len(errors): #if there are any errors return user to homepage to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('homepage'))
    else: #login user
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['alias'] = user.alias
    return redirect(reverse('book_index'))

#show all books
def show_books(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #get list of all books (including reviews -- will require JOIN somehow)
    recent_reviews = Review.objects.all().order_by("-created_at")[:3].values_list("id", flat=True)
    other_reviews = Review.objects.exclude(pk__in=list(recent_reviews))
    context = {'books': Book.objects.all(), 'last_reviewed': Review.objects.all().order_by("-created_at")[:3], 'other_reviews': other_reviews }
    return render(request, 'books/all_books.html', context)

#show new_book form
def new(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    context = {'authors': Author.objects.all()}
    return render(request, 'books/new.html', context)

#create new book
def create_book(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #validate data
    request.session['newbookauthor'] = request.POST['author_new']
    request.session['newbookreview'] = request.POST['review']
    request.session['newbookrate'] = request.POST['rating']
    reviewer_id = request.session['user_id']
    errors = Book.objects.newbook_valid(request.POST)
    if len(errors):  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('new_book'))
    else: #add a new book
        book = Book.objects.create_book(request.POST, reviewer_id)
        book_id = book.id
        #delete session data for new book, no longer needed
        del request.session['newbooktitle']
        del request.session['newbookauthor'] 
        del request.session['newbookreview'] 
        del request.session['newbookrate'] 
        return redirect(reverse('book_details', kwargs={'book_id':book_id}))

#show single book details
def show_book(request, book_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #get the books, including reviews
    context = {'book': Book.objects.get(id=book_id), 'reviews': Review.objects.filter(book_id=book_id).order_by("-created_at")[:3]}
    return render(request, 'books/book.html', context)

#update book with new review
def update(request, book_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    reviewer_id = request.session['user_id']
    #validate data
    errors = Book.objects.valid_review(request.POST)
    if len(errors):  #if there are any errors return user to index.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('book_details'))
    else: #add new review
        Book.objects.add_review(book_id, reviewer_id, request.POST)
    return redirect(reverse('book_details', kwargs={'book_id':book_id}))

#show user
def show_user(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #get the user details, including books reviewed
    count = Review.objects.filter(reviewer_id=user_id).count()
    context = {'user': User.objects.get(id=user_id), 'user_reviews': Book.objects.filter(book_reviews__reviewer_id=user_id), "num_reviews": count}
    return render(request, 'books/user_reviews.html', context)

#delete a review owned by user
def destroy(request, review_id, book_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(reverse('book_details', kwargs={'book_id':book_id}))

#log user out
def logout(request):
    #clear all session information
    for i in request.session.keys():
        del request.session[i]
    return redirect(reverse('homepage'))