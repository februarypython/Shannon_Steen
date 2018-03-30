# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class PostMananger(models.Manager):
    def valid_message(self, postData):
        errors = {}
        if len(postData['Post'] < 1): #null
            errors['no_msg'] = "Oops, you forgot to enter your message. Please do so now."
        return errors

    def add_message(self, postData, to_user, from_user):
        msg_from = User.objects.get(id=from_user)
        msg_to = User.objects.get(id=to_user)
        this_msg = self.create(Post=postData['Post'], msg_from=msg_from, msg_to=msg_to)
        return this_msg 

class Post(models.Model):
    message = models.TextField()
    msg_from = models.ForeignKey(User, related_name="posted", on_delete=models.CASCADE)
    msg_to = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Message Info: %s written by %s' % (self.message, self.messenger)