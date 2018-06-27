import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User


class Artical(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  active = models.BooleanField(default=True)
  author = models.ForeignKey(User, on_delete=False, blank=True, null=True)
  title = models.CharField(max_length=200)
  created_date = models.DateTimeField(default=datetime.datetime.now())
  content = models.TextField()
  last_modified = models.DateTimeField(auto_now=True)

  def author_name(self):
  	return self.author.name

  def __str__(self):
     return self.title 

  class Meta:
    db_table = 'Artical'


class Vote(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=False)
  artical = models.ForeignKey(Artical, on_delete=False)
  up_vote = models.BooleanField(default=True, null=False, blank=False)

  def __str__(self):
  	return self.id

  class Meta:
    db_table = 'Vote'
