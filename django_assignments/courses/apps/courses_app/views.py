# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import Course, Description

# Create your views here.
def index(request):
    return HttpResponse("got a lot of work to do")