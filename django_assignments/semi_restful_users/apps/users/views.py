# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages  #for flashing error messages
from .models import User

# Create your views here.

#show all users
def index(request):
    #query for users
    context = {'users':User.objects.all()}
    return render(request, 'users/index.html', context)

#display form for adding new user
def new(request):
    return render(request, 'users/new.html')

#create the new user
def create(request):
    #run validation
    errors = User.objects.basic_validator(request.POST)
    #if there are any errors return user to new.html to correct
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('new_user'))
    else:
        User.objects.create_user(request.POST['first_name'], request.POST['last_name'], request.POST['email'])
        return redirect(reverse('user_index'))

#show a specific user
def show(request, user_id):
    context = {'user': User.objects.get(id=user_id)}
    return render(request, 'users/show.html', context)

#display form to edit specific user
def edit(request, user_id):
    #get specific user information
    context = {'user': User.objects.get(id=user_id)}
    #use session to pass user_id to update route in lieu of passing through url
    request.session['id'] = user_id
    print request.session['id']
    return render(request, 'users/edit.html', context)

#update the specifc user and return to show
def update(request):
    print request.session['id']
    user = User.objects.get(id=request.session['id'])
    #validate new data input
    new_errors = User.objects.validate_changes(request.POST)
    #if there are any errors return user to edit.html to correct
    if len(new_errors):
        for tag, error in new_errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('edit_user', kwargs={'user_id':request.session['id']}))
    else:  #proceed with changes
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        # del request.session['id'] #pop out id as no longer needed
        return redirect(reverse('show_user', kwargs={'user_id':request.session['id']
}))

#delete the user
def destroy(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect(reverse('user_index'))