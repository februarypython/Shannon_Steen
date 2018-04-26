# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User
from ..communiques.models import Communique

# Create your models here.
class CommentManager(models.Manager):
    def valid_comment(self, post_data):
        errors = {}
        if len(post_data['comment']) < 1: #null
            errors['no_comment'] = "Oops, you forgot to enter your comment. Please do so now."
        return errors

    def add_comment(self, post_data, msg_id, user_id):
        this_msg = Communique.objects.get(id=msg_id)
        this_user = User.objects.get(id=user_id)
        this_comment = self.create(comment=post_data['comment'], communique=this_msg, commenter=this_user)
        return this_msg 

class Comment(models.Model):
    comment = models.TextField()
    communique = models.ForeignKey(Communique, related_name="communiques", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #connect instance of CommentsManager overwriting old objects key with new properties
    objects = CommentManager()

    def __str__(self):
        return 'Comment %s Info: %s written by %s on %s' % (self.id, self.comment, self.commenter, self.communique)
