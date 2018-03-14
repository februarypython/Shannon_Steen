# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
import random  #for purposes of generating an order id; normally this wouldn't be required as would be working with a db

# Create your views here.
def index(request):
    inventory = [   #load some inventory; normally this wouldn't be required as would be working with a db
        {"id": 2, "product": 'Nine West Emmala', "image": '/static/amadon/images/emmalalace.jpg', "price": 79.21, "color": 'cream', "style": "pumps"},
        {"id": 3, "product": 'Nine West Emmala', "image": '/static/amadon/images/emmalaorange.jpg', "price": 89.00, "color": 'orange', "style": "pumps"},
        {"id": 6, "product": 'Ted Baker Hallden', "image": '/static/amadon/images/halldenpalace.jpg', "price": 187.00, "color": 'floral', "style": 'pumps'},
        {"id": 16, "product": 'Steve Madden Slithur', "image": '/static/amadon/images/stevemaddenred.jpg', "price": 85.95, "color": 'red', "style": 'sandals'},
        {"id": 4, "product": 'Calvin Klein Ginette', "image": '/static/amadon/images/ginetteblack.jpg', "price": 67.63, "color": 'black', "style": 'mules'},
        {"id": 5, "product": 'Calvin Klein Ginette', "image": '/static/amadon/images/ginettesand.jpg', "price": 98.99, "color": 'sand', "style": 'mules'},
        {"id": 1, "product": 'Aldo Cardross', "image": "/static/amadon/images/aldogold.jpg", "price": 151.20, "color": 'gold', "style": 'sandals'},
        {"id": 7, "product": 'Nine West Janissah', "image": '/static/amadon/images/janissahblack.jpg', "price": 79.00, "color": 'black', "style": 'wedges'},
        {"id": 8, "product": 'Nine West Janissah', "image": '/static/amadon/images/janissahorange.jpg', "price": 79.00, "color": 'orange', "style": 'wedges'},
        {"id": 9, "product": 'Nine West Janissah', "image": '/static/amadon/images/janissahtaupe.jpg', "price": 79.00, "color": 'taupe', "style": 'wedges'},
        {"id": 12, "product": 'Bandolino Rainaa', "image": '/static/amadon/images/rainaagold.jpg', "price": 39.99, "color": 'gold', "style": 'pumps'},
        {"id": 13, "product": 'Bandolino Rainaa', "image": '/static/amadon/images/rainaagunmetal.jpg', "price": 45.99, "color": 'gunmetal', "style": 'pumps'},
        {"id": 14, "product": 'Imagine Vince Camuto Rashi', "image": '/static/amadon/images/rashiwhite.jpg', "price": 169.89, "color": 'white', "style": 'sandals'},
        {"id": 15, "product": 'Imagine Vince Camuto Rashi', "image": '/static/amadon/images/rashigold.jpg', "price": 169.89, "color": 'gold', "style": 'sandals'},
        {"id": 17, "product": 'Imagine Vince Camuto Dayanara', "image": '/static/amadon/images/dayanarablack.jpg', "price": 169.89, "color": 'black', "style": 'sandals'},
        {"id": 18, "product": 'Imagine Vince Camuto Dayanara', "image": '/static/amadon/images/dayanarawhite.jpg', "price": 169.89, "color": 'white', "style": 'sandals'},
        {"id": 11, "product": 'Chloe Gosselin Enchysia', "image": '/static/amadon/images/chloegosselin.jpg', "price": 689.99, "color": 'black', "style": 'pumps'},
        {"id": 10, "product": 'Coach Waverly Tea Rose', "image": '/static/amadon/images/coachsage.jpg', "price": 238.00, "color": 'sage', "style": 'pumps'},
    ]
    if 'inventory' not in request.session: #initialize the inventory
        request.session['inventory'] = inventory
    if 'cart' not in request.session: #initialize the cart
        request.session['cart'] = []
    if 'order_history' not in request.session: #initialize the order_history (all history)
        request.session['order_history'] = []
    if 'order_details' not in request.session: #initialize the order_details (order specific)
        request.session['order_details'] = []
    if 'order_id' not in request.session: #create an order #
        request.session['order_id'] = random.randint(5000, 10000)
    context = {'inventory':request.session['inventory']}
    request.session['order_id']
    return render(request, 'amadon/index.html', context)   

def add(request, item_id):
    found_in_cart = False
    if request.method == 'POST':
        request.session.modified = True #must add this to save session data changes made on backend
        if request.session['cart'] != []:  #cart is not empty
            for cart_item in range(len(request.session['cart'])): #check if item is already in cart
                if request.session['cart'][cart_item]['item_id'] == int(item_id):  #this item is in cart, update quantity/total price
                    found_in_cart = True
                    request.session['cart'][cart_item]['quantity'] += 1
                    request.session['cart'][cart_item]['total_price'] = request.session['cart'][cart_item]['price'] * request.session['cart'][cart_item]['quantity'] #base inventory price * quantity
                    break #cart quantity/total price updated, break out of loop
        if found_in_cart == False: #item wasn't in cart
            for item in range(len(request.session['inventory'])): #find the item in our inventory
                if request.session['inventory'][item]['id'] == int(item_id): #find the item details in inventory to add to our cart
                    request.session['cart'].append({'order_id': request.session['order_id'], 'item_id': request.session['inventory'][item]['id'], 'product': request.session['inventory'][item]['product'], 'image': request.session['inventory'][item]['image'], 'quantity': 1, 'price': request.session['inventory'][item]['price'], 'total_price': request.session['inventory'][item]['price'], 'style': request.session['inventory'][item]['style']})
    return redirect('/amadon/cart')

def show_cart(request):
    request.session['cart_count'] = 0  #inialize total items count
    request.session['cart_total'] = 0 #intialize total price
    for cart_item in range(len(request.session['cart'])): #count and sum all items in cart
        request.session['cart_count'] += int(request.session['cart'][cart_item]['quantity']) #count all items in the cart
        request.session['cart_total'] += request.session['cart'][cart_item]['total_price'] #total all items in the cart
    context = {'cart':request.session['cart'], 'count': request.session['cart_count'], 'total': request.session['cart_total']}
    return render(request, 'amadon/cart.html', context)

def update(request, item_id):
    if request.method == 'POST':
        request.session.modified = True #must add this to save session data changes made on backend
        for cart_item in range(len(request.session['cart'])): #find the item to update in the cart
            if request.session['cart'][cart_item]['item_id'] == int(item_id):  #update quantity/total price
                if int(request.POST['quantity']) == 0:  #in case user changes quantity to 0 rather than selecting remove button
                    request.session['cart'].pop(cart_item)  #pop item out of the cart
                else:
                    request.session['cart'][cart_item]['quantity'] = request.POST['quantity']
                    request.session['cart'][cart_item]['total_price'] = request.session['cart'][cart_item]['price'] * int(request.POST['quantity']) #base inventory price * quantity
                break #cart quantity/total price updated, break out of loop
    return redirect('/amadon/cart')

def remove(request, item_id):
    if request.method == 'POST':
        request.session.modified = True #must add this to save session data changes made on backend
        for cart_item in range(len(request.session['cart'])): #find the item to update in the cart
            if request.session['cart'][cart_item]['item_id'] == int(item_id):  
                request.session['cart'].pop(cart_item)  #pop item out of the cart
    return redirect('/amadon/cart')

def checkout(request):
    if 'ytd_count' not in request.session: #create the ytd_count session
        request.session['ytd_count'] = 0
    if 'ytd_total' not in request.session: #create the ytd_total session
        request.session['ytd_total'] = 0
    request.session['ytd_count'] += int(request.session['cart_count'])  #update ytd_count with most recent purchase
    request.session['ytd_total'] += float(request.session['cart_total'])  #update ytd_total with most recent purchase
    request.session['order_history'].append(request.session['cart'])
    context = {'cart':request.session['cart'], 'count': request.session['cart_count'], 'total': request.session['cart_total'], 'ytd_count':request.session['ytd_count'], 'ytd_total': request.session['ytd_total'], 'order_id': request.session['order_id']}
    del request.session['cart']  #empty cart for next purchasing session
    del request.session['order_id'] #reset order_id for next purchase session
    return render(request, 'amadon/checkout.html', context)

def show_order(request, order_id):
    # request.session.modified = True #must add this to save session data changes made on backend

    for order in range(len(request.session['order_history'])):
        for details in range(len(request.session['order_history'][order])):  #orders are pushed as list items so must drill down a level
            if request.session['order_history'][order][details]['order_id'] == int(order_id):  #find all items in the order
                request.session['order_details'].append(request.session['order_history'][order][details])
    context = {'order_details':request.session['order_details'], 'order_id': order_id}
    return render(request, 'amadon/order.html', context)