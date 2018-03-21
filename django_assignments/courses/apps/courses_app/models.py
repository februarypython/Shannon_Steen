# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CourseManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 6:
            print "course name not valid"
            errors['name'] = "Please enter a valid course name. Course names must be more than 5 characters long."
        if len(postData['description']) < 16:
            print "description is not complete"
            errors['desc'] = "Please enter a complete description of the course name. Descriptions should be a more than 15 characters long."
        return errors
    
    def add_course(self, cname, cdesc):
        course = self.create(course_name=cname, course_desc=Description.objects.create(cdesc))
        return course

class Description(models.Model):
    course_desc = models.TextField()

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_desc = models.OneToOneField(Description, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #connect instance of CourseManager overwriting old objects key with new properties
    objects = CourseManager()

    def __str__(self):
        return "Course Info:  %s %s" % (self.course_name, self.course_desc)