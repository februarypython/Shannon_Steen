# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages  #for flashing error messages
from .models import Communique  #import communique model
from ..users.models import User  #import user model
from ..comments.models import Comment  #import comment model

# Create your views here.

#create new message
def create(request, msg_to_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    from_id = request.session['user_id']
    #validate data
    errors = Communique.objects.valid_message(request.POST)
    if len(errors):  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags='bad_msg')
        return redirect('users:show', kwargs={'user_id':msg_to_id})
    else: #add a new book
        new_msg = Communique.objects.add_message(request.POST, msg_to_id, from_id)
        return redirect('users:show', kwargs={'user_id':msg_to_id})

def show(request, user_id):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    context = {
        'user': User.objects.get(id=user_id),
        'msg_rcvd': Communique.objects.filter(msg_to=user_id).filter(has_been_archived=1).order_by('-created_at'),
        'comments': Comment.objects.all(),
        'unread': Communique.objects.filter(msg_to=request.session['user_id']).filter(has_been_read=False).count(),
    }
    return render(request, 'communiques/show.html', context)

def edit(request, message_id):
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    previous_page = request.META['HTTP_REFERER']
    msg = Communique.objects.get(id=message_id)
    msg.has_been_read = True
    msg.save()
    return redirect(previous_page)

#archive message
def update(request, message_id):
    if 'user_id' not in request.session:
        return redirect('login_registration:homepage')
    previous_page = request.META['HTTP_REFERER']
    msg = Communique.objects.get(id=message_id)
    msg.has_been_read = True
    msg.has_been_archived = True
    msg.save()
    return redirect(previous_page)