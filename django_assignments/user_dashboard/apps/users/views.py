# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages  #for flashing error messages
from .user_models import User  #import user model

# Create your views here.

#show home page
def index(request):
    return render(request, 'users/index.html')

#show add_new form
def register(request):
    context = {
        'page_title': 'Register'
    }
    return render(request, 'users/new.html', context)

#login existing user
def login(request):
    if request.method == 'POST':
        #validate login
        errors = User.objects.login_valid(request.POST)
        if len(errors): #if there are any errors return user to login to correct
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect(reverse('login'))
        else: #login user
            user = User.objects.get(email=request.POST['email'])
            print user
            request.session['user_id'] = user.id
            if user.user_level == 9: # admin level
                print "this is an admin level user"
                return redirect(reverse('admin_dashboard'))
            else:
                print "this is not an admin level user"
                return redirect(reverse('user_dashboard'))
    else:
        return render(request, 'users/login.html')

#show 
def show(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    if User.objects.get(id=request.session['user_id']).user_level == 9:  #user is an admin, tweak page to show admin options
        page_title = "Admin Dashboard"
        permission = "admin"
    else:
        page_title = "User Dashboard"
        permission = "user"
    context = {
        'users': User.objects.all(),
        'permission': permission, 
        'page_title':  page_title,
    }
    return render(request, 'users/show.html', context)

#show add_new form
def new(request):
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    context = {
        'page_title': 'New User',
    }
    return render(request, 'users/new.html', context)

#create new 
def create(request):
    previous_page = request.META['HTTP_REFERER']
    print previous_page
    #validate data
    request.session['formdata'] = request.POST
    errors = User.objects.registration_valid(request.POST)
    if len(errors): #if there are any errors return user to register to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(previous_page)
    else: #add new user
        user = User.objects.create_user(request.POST)
        request.session['user_id'] = user.id
        del request.session['formdata'] 
        return redirect(reverse('user_dashboard'))


#show edit form
def edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    if User.objects.get(id=request.session['user_id']).user_level == 9:  #user is an admin, tweak page to show admin options
        page_title = "Edit User"
        permission = "admin"
    else:
        page_title = "Edit Profile"
        permission = "user"
    context = {
        'page_title': page_title,
        'permission': permission,
        'user_info': User.objects.get(id=user_id)
    }
    return render(request, 'users/edit.html', context)

#update user
def update(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    previous_page = request.META['HTTP_REFERER']
    print previous_page
    #validate data
    request.session['formdata'] = request.POST


    errors = MODEL.objects.MODELMETHOD_valid(request.POST)
    if len(errors):  #if there are any errors return user to index.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('book_details'))
    else: #add new
        WHAT = MODEL.objects.MODELMETHOD_create(request.POST)
    return redirect(reverse('show_details', kwargs={'IF_NEEDED':arg_id}))

#delete a review owned by user
def destroy(request, review_id, book_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    WHAT = MODEL.objects.get(id=review_id)
    WHAT.delete()
    return redirect(reverse('show_details', kwargs={'IF_NEEDED':arg_id}))

#log user out
def logout(request):
    #clear all session information
    for i in request.session.keys():
        del request.session[i]
    return redirect(reverse('homepage'))