# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0  #initialize the counter
    return render(request, 'surveys/index.html')

def process(request):
    if request.method == 'POST':  #user has completed form, process data
        request.session['counter'] += 1  #count number of times user submits
        request.session['name'] = request.POST['name']
        request.session['location'] = request.POST['dojo_location']
        request.session['language'] = request.POST['favorite_language']
        request.session['comment'] = request.POST['comment']
        return redirect('/result')
    else:  #accessed page via get, no form data, redirect to root route
        return redirect('/')

def result(request):
    return render(request, 'surveys/result.html')