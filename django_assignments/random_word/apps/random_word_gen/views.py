# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.utils.crypto import get_random_string


# Create your views here.
def index(request):
    request.session['counter'] += 1  #initialize the counter
    request.session['rand_word'] = get_random_string(length=14)  #get random word
    print request.session['counter']
    print request.session['rand_word']
    return render(request, 'random_word_gen/index.html')

def reset(request):
    request.session['counter'] = 0  #reset the counter
    return redirect('/random_word')