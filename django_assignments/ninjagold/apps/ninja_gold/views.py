# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
import random #for calculating wins/losses
from datetime import datetime

# Create your views here.
def index(request):
    if 'ninja_gold' not in request.session: #first visit, initialize ninja_gold
        request.session['ninja_gold'] = 0
    if 'ninja_activities' not in request.session: #first visit, inialize activities
        request.session['ninja_activities'] = []
    context = {
        'gold': request.session['ninja_gold'],
        'activities': request.session['ninja_activities']
    }
    return render(request, 'ninja_gold/index.html', context)

def process_money(request, building):
    request.session.modified = True #must add this to save session data changes made on backend
    dt = datetime.strftime(datetime.now(), "%Y/%m/%d, %I:%M %p")
    if building == 'farm':  #user went to the farm
        farm_gold = random.randint(10, 20) #credit random about between 10-20
        request.session['ninja_gold'] += farm_gold
        request.session['ninja_activities'].append({'activity': "Earned {} golds from the farm! {}".format(farm_gold, dt), 'class': 'wins'})
    elif building == 'cave':  #user went to the cave
        cave_gold = random.randint(5, 10) #credit random about between 5-10
        request.session['ninja_gold'] += cave_gold
        request.session['ninja_activities'].append({'activity': "Earned {} golds from the cave! {}".format(cave_gold, dt), 'class': 'wins'})
    elif building == 'house':  #user went to the house
        house_gold = random.randint(2, 5) #credit random about between 2-5
        request.session['ninja_gold'] += house_gold
        request.session['ninja_activities'].append({'activity': "Earned {} golds from the house! {}".format(house_gold, dt), 'class': 'wins'})
    else:   #user went to the casino
        casino_gold = random.randint(-50, 50) #credit/debit random about between -50 to 50
        request.session['ninja_gold'] += casino_gold
        if casino_gold < 0:  #lost money in casino
            request.session['ninja_activities'].append({'activity': "Entered a casino and lost {} golds... Ouch! {}".format(casino_gold, dt), 'class': 'losses'})
        else: #won money in casino
            request.session['ninja_activities'].append({'activity': "Entered a casino and won {} golds... Sweet! {}".format(casino_gold, dt), 'class': 'wins'})
    return redirect('/')