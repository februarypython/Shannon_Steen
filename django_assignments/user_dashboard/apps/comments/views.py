# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages  #for flashing error messages
from ..users.decorators import required_login #import decorator function
from ..users.models import User  #import user model
from ..communiques.models import Communique  #import communique model
from .models import Comment  #import comment model


# Create your views here.

#create new comment
@required_login
def create(request, msg_id):
    user_id = request.session['user_id']
    previous_page = request.META['HTTP_REFERER']
    #validate data
    errors = Comment.objects.valid_comment(request.POST)
    if errors:  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags='bad_comment')
        return redirect(previous_page)
    else: #add a new book
        new_comment = Comment.objects.add_comment(request.POST, msg_id, user_id)
        return redirect(previous_page)

#delete a comment
@required_login
def destroy(request, cmt_id):
    previous_page = request.META['HTTP_REFERER']
    comment = Comment.objects.get(id=cmt_id)
    comment.delete()
    return redirect(previous_page)