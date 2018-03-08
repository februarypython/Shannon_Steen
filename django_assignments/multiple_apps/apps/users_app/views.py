# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

# /login - display 'placeholder for users to login' 
def index(request):
    return HttpResponse("placeholder for users to login")

# /users/new - have the same method that handles /register also handle the url request of /users/new
# /register - display 'placeholder for users to create a new user record'
def new(request):
    response = "placeholder for users to create a new user record"
    return HttpResponse(response)

# /users - display 'placeholder to later display all the list of users'
def show(request):
    return HttpResponse("placeholder to later display all the list of users")