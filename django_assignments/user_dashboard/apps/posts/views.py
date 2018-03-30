# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages  #for flashing error messages
from .models import Post  #import user model

# Create your views here.

#create new message
def create(request, user_id):
    previous_page = request.META['HTTP_REFERER']
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #validate data
    errors = Post.objects.message_valid(request.POST)
    if len(errors):  #if there are any errors return user to new.html to correct
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('previous_page'))
    else: #add a new message
        new_msg = Post.objects.add_message(request.POST, to_user=user_id, from_user=request.session['id'])
        return redirect(reverse('previous_page'))

#update book with new review
def update(request):
    #ensure user is in session
    if 'user_id' not in request.session:
        return redirect(reverse('homepage'))
    #validate data
    # THIS IS ONLY NEEDED IF VALIDATING NEW INPUT (i.e. wouldn't need on table like 'comments')
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