# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages  #for flashing error messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'registration/index.html')

def create(request):
    #save form data in session to return values to form
    request.session['form_fname'] = request.POST['first_name']
    request.session['form_lname'] = request.POST['last_name']
    request.session['form_email'] = request.POST['email']
    request.session['form_dob'] = request.POST['birthdate']
    errors = User.objects.registration_valid(request.POST)
    if len(errors):  #if there are any errors return user to index.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('view_index'))
    else:
        user = User.objects.create_user(request.POST)
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['result'] = "You have successfully registered."
        return redirect(reverse('success'))

def show(request):
    errors = User.objects.login_valid(request.POST)
    if len(errors):  #if there are any errors return user to index.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('view_index'))
    else:
        #get the user, save id and name to session
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['result'] = "You have successfully logged in."
        return redirect(reverse('success'))

def success(request):
    context = {'result': request.session['result'], 'first_name': request.session['first_name']}
    for i in request.session.keys(): #clear all data in session
        del request.session[i]
    return render(request, 'registration/success.html', context)