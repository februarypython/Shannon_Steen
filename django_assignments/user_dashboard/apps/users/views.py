# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages  #for flashing error messages
from .models import User  #import user model
from ..communiques.models import Communique #import communique model
from ..comments.models import Comment #import comment model

#Create your views here.

#show add_new form
def new(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    context = {
        'page_title': 'New User',
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
    }
    return render(request, 'users/new.html', context)

#create new user
def create(request):
    previous_page = request.META['HTTP_REFERER']
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
        if 'user_id' not in request.session:  #new user registering for site
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            request.session['license'] = user.user_level
        return redirect('login_registration:dashboard')

def show(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    context = {
        'user': User.objects.get(id=user_id),
        'msg_rcvd': Communique.objects.filter(msg_to=user_id).order_by('-created_at'),
        'comments': Comment.objects.all(),
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
        'msg_ct': Communique.objects.filter(msg_to=request.session['user_id']).count(),
    }
    return render(request, 'users/show.html', context)

#show edit form
def edit(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    if request.session['license'] == 9:  #user is an admin, tweak page to show admin options
        permission = "admin"
        page_title = "Edit User"
        if int(user_id) == request.session['user_id']:
            page_title = "Edit Profile"
    else:
        page_title = "Edit Profile"
        permission = "user"
    context = {
        'page_title': page_title,
        'permission': permission,
        'user_info': User.objects.get(id=user_id),
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
    }
    return render(request, 'users/edit.html', context)

#update user
def update(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
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

#delete a user
def destroy(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('login_registration:dashboard')