# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages  #for flashing error messages
from .user_models import User  #import user model

#Create your views here.

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
            request.session['name'] = user.first_name
            request.session['license'] = user.user_level
            return redirect(reverse('dashboard'))
    else:
        return render(request, 'users/login.html')

#show 
def show(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    if request.session['license'] == 9:  #user is an admin, tweak page to show admin options
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

def show_user(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    if request.session['license'] == 9:  #user is an admin, tweak page to show admin options
        page_title = "Admin Dashboard"
        permission = "admin"
    else:
        page_title = "User Dashboard"
        permission = "user"
    context = {
        'users': User.objects.get(id=user_id),
        'permission': permission, 
        'page_title':  page_title,
    }
    return render(request, 'users/index.html', context)

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
        del request.session['formdata'] 
        if 'user_id' not in session:  #new user registering for site
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            request.session['license'] = user.user_level
        return redirect(reverse('dashboard'))

#show edit form
def edit(request, **kwargs):
    chosen_path = request.path
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    if request.session['license'] == 9:  #user is an admin, tweak page to show admin options
        page_title = "Edit User"
        permission = "admin"
    else:
        page_title = "Edit Profile"
        permission = "user"
    if not kwargs:  #user level permissions, get id stored in session
        user_id = request.session['user_id']
    else: #admin level permissions, get from url
        user_id = kwargs['user_id']
    context = {
        'page_title': page_title,
        'permission': permission,
        'user_info': User.objects.get(id=user_id),
        'path': chosen_path,
    }
    return render(request, 'users/edit.html', context)

#update user
def update(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    previous_page = request.META['HTTP_REFERER']
    #determine which form was updated and validate data
    if 'update-info' in request.POST:  #this is the edit info form
        info_errors = User.objects.update_user_info(request.POST, user_id)
        if len(info_errors):  #if there are any errors return user to index.html to correct
            for tag, error in info_errors.items():
                messages.error(request, error, extra_tags='bad_info')
                return redirect(previous_page)
        else:  #make the changes
            messages.success(request, "User Information has been updated.", 'info_success')
    if 'update-password' in request.POST: #determine which form updated - this is the change password form
        pw_errors = User.objects.update_password(request.POST, user_id)
        if len(pw_errors):  #if there are any errors return user to index.html to correct
            for tag, error in pw_errors.items():
                messages.error(request, error, extra_tags='bad_pw')
                return redirect(previous_page)
        else:  #make the changes
            messages.success(request, "Password has been updated.", 'pw_success')
    if 'update-desc' in request.POST:  #determine which form updated - this is the edit desc form
        #no need to validate, make the changes
        user = User.objects.get(id=user_id)
        user.description = request.POST['desc']
        user.save()
        messages.success(request, "User Description has been updated.", 'desc_success')
    return redirect(previous_page)

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