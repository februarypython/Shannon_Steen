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
    
    def add_course(self, postData):
        desc = Description.objects.create(course_desc=postData['description'])
        course = Course.objects.create(course_name=postData['name'], course_desc=desc)
        return course

    def add_comment(self, postData, course_id,):
        print postData
        new_comment = Comment.objects.create(comment=postData['comment'], course=course_id)
        print new_comment
        return new_comment

class Description(models.Model):
    course_desc = models.TextField()
    
    def __str__(self):
        return self.course_desc

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_desc = models.OneToOneField(Description, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #connect instance of CourseManager overwriting old objects key with new properties
    objects = CourseManager()

    def __str__(self):
        return "Course Info:  %s %s" % (self.course_name, self.course_desc)

class Comment(models.Model):
    comment = models.TextField()
    course = models.ForeignKey(Course, related_name="courses")
    
    def __str__(self):
        return self.comment