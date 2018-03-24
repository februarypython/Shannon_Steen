# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Course, Description, Comment
from django.contrib import messages #for flashing error messages


# Create your views here.

#show all courses and form for adding new
def index(request):
    context = {'courses': Course.objects.all()}
    return render(request, 'courses_app/index.html', context)

#create new course
def create(request):
    #run validation
    errors = Course.objects.basic_validator(request.POST)
    #if there are any errors, return to index.html to correct
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('course_index'))
    else:
        Course.objects.add_course(request.POST)
        return redirect(reverse('course_index'))

#show course details with comments
def show(request, course_id):
    context = {'course': Course.objects.get(id=course_id), 'comments': Comment.objects.filter(course=course_id)}
    print context
    return render(request, 'courses_app/details.html', context)

#add comments via update method
def update(request, course_id):
    course = Course.objects.get(id=course_id)
    comment = Course.objects.add_comment(request.POST, course)
    return redirect(reverse('show_course', kwargs={'course_id':course_id}))


#display remove.html
def confirm(request, course_id):
    context = {'course': Course.objects.get(id=course_id)}
    return render(request, 'courses_app/remove.html', context)

#delete course and return to course index
def destroy(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect(reverse('course_index'))