# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages  #for flashing error messages
from ..users.models import User  #import user model
from .models import Communique  #import communique model

# Create your views here.

#create new message
def create(request, msg_to_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('login_registration:homepage'))
    previous_page = request.META['HTTP_REFERER']
    from_id = request.session['user_id']
    #validate data
    errors = Communique.objects.valid_message(request.POST)
    if len(errors):  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags='bad_msg')
        return redirect(reverse('users:show', kwargs={'user_id':msg_to_id}))
    else: #add a new book
        new_msg = Communique.objects.add_message(request.POST, msg_to_id, from_id)
        return redirect(reverse('users:show', kwargs={'user_id':msg_to_id}))