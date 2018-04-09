# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class CommuniqueManager(models.Manager):
    def valid_message(self, post_data):
        errors = {}
        if len(post_data['message']) < 1: #null
            errors['no_msg'] = "Oops, you forgot to enter your message. Please do so now."
        return errors

    def add_message(self, post_data, to_user, from_user):
        if 'private' in post_data:  #user marked private message
            priv = 0
        else:
            priv = 1
        msg_from = User.objects.get(id=from_user)
        msg_to = User.objects.get(id=to_user)
        this_msg = self.create(message=post_data['message'], privacy=priv, msg_from=msg_from, msg_to=msg_to)
        return this_msg 

class Communique(models.Model):
    STATUS_CHOICES = (
        (0, 'private'),
        (1, 'public'),
    )
    message = models.TextField()
    msg_from = models.ForeignKey(User, related_name="written_msgs", on_delete=models.CASCADE)
    msg_to = models.ForeignKey(User, related_name="received_msgs", on_delete=models.CASCADE)
    privacy = models.IntegerField(choices=STATUS_CHOICES, default=1)
    has_been_read = models.BooleanField(default=False)
    has_been_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of UserManager overwriting old objects key with new properties
    objects = CommuniqueManager()

    def __str__(self):
        return 'Message %s: %s to %s written by %s' % (self.id, self.message, self.msg_to, self.msg_from)