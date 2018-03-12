# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime

# Create your views here.
def index(request):
    if 'words_added' not in request.session: #create the session
        request.session['words_added'] = []
    context = {'activities': request.session['words_added']}
    return render(request, 'words/index.html', context)

def process(request):
    if request.method == 'POST':
        request.session['date'] = datetime.strftime(datetime.now(), '%B %d, %Y')
        request.session['time'] = datetime.strftime(datetime.now(), '%I:%M:%S %p')
        request.session['new_word'] = request.POST['new_word'] #capture the new word
        request.session['color'] = request.POST['color'] #capture the color choice
        if 'big_fonts' in request.POST: #user has chosen big fonts
            request.session['big_fonts'] = 'big'
        else:
            request.session['big_fonts'] = 'normal'
        #append new data to dict
        request.session['words_added'].append({'word': request.session['new_word'], 'color': request.session['color'], 'big_fonts': request.session['big_fonts'], 'time': request.session['time'], 'date': request.session['date']})
    return redirect('/session_words')

def clear(request):
    for i in request.session.keys(): #clear all data in session
        del request.session[i]
    return redirect('/session_words')