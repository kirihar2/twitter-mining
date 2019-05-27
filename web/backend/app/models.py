# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class GPIO(models.Model):
    GPIO_Pin = models.CharField(max_length=200)
    toggle_on = models.BooleanField(default = True)
    pub_date = models.DateTimeField('date published')

class item(models.Model):

    extension = models.CharField(max_length=5)
    file_name = models.CharField(max_length=2000)
    version = models.IntegerField()

class joke(models.Model):
    text = models.CharField(max_length=3000)
    generated_version = models.IntegerField()

