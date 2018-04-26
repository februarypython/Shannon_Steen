# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages  #for flashing error messages
from ..users.models import User  #import user model
from ..communiques.models import Communique #import communique model
from ..users.decorators import required_login #import decorator function

#Create your views here.

#show home page
def index(request):
    if 'user_id' in request.session:
        context = {
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
        }
        return render(request, 'login_registration/homepage.html', context)
    return render(request, 'login_registration/homepage.html')

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
        if errors: #if there are any errors return user to login to correct
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect('login_registration:login')
        else: #login user
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            request.session['license'] = user.user_level
            return redirect('login_registration:dashboard')
    else:
        return render(request, 'login_registration/login.html')

#show all users
@required_login
def show(request):
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
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
    }
    return render(request, 'login_registration/index.html', context)

#log user out
def logout(request):
    #clear all session information
    for i in request.session.keys():
        del request.session[i]
    return redirect('login_registration:homepage')