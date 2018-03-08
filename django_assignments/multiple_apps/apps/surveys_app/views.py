# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

# /surveys - display "placeholder to display all the surveys created"
def index(request):
    return HttpResponse("placeholder to display all the surveys created")

# /surveys/new - display "placeholder for users to add a new survey"
def new(request):
    return HttpResponse("placeholder for users to add a new survey")