# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
# Create your views here.


def index(request):
    time_data = {
        'date': datetime.strftime(datetime.now(), '%b %d, %Y'),
        'time': datetime.strftime(datetime.now(), '%I:%M %p')    
    }
    print time_data
    print time_data
    return render(request, 'timedisplay/index.html', time_data)