# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    wg_user = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
class UserStat(models.Model):
    wg_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ship_id = models.BigIntegerField(default=0, db_index=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)