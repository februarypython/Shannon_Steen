# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
import re # for testing/matching regular expressions
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.first_name < 1: #user didn't enter first name
            raise ValidationError(_("Please enter a first name."))
        if self.last_name < 1: #user didn't enter last name
            raise ValidationError(_("Please enter a last name."))
        if self.email_address < 1 or not EMAIL_REGEX.match(self.email_address):
            raise ValidationError(_("Please enter a valid email address."))