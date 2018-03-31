# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages  #for flashing error messages
from ..users.models import User  #import user model
from ..communiques.models import Communique  #import communique model
from .models import Comment  #import comment model


# Create your views here.

#create new comment
def create(request, msg_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('login_registration:homepage'))
    user_id = request.session['user_id']
    previous_page = request.META['HTTP_REFERER']
    #validate data
    errors = Comment.objects.valid_comment(request.POST)
    if len(errors):  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags='bad_comment')
        return redirect(previous_page)
    else: #add a new book
        new_comment = Comment.objects.add_comment(request.POST, msg_id, user_id)
        return redirect(previous_page)