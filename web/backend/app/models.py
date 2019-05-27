# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class GPIO(models.Model):
    GPIO_Pin = models.CharField(max_length=200)
    toggle_on = models.BooleanField(default = True)
    pub_date = models.DateTimeField('date published')

class trained_version(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    extension = models.CharField(max_length=5)
    filename = models.CharField(max_length=2000)
    version = models.IntegerField()
    @classmethod
    def create(cls, version, filename):
        tr = cls(extension='hdf5',filename=filename,version=version)
        return tr
   

class generated_joke(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=3000)
    generated_version = models.ForeignKey(trained_version, on_delete=models.CASCADE)
    create_date = models.DateTimeField('date created')
    @classmethod
    def create(cls,text,generated_version,create_date):
        joke = cls(text=text,generated_version=generated_version,create_date=create_date)
        return joke
    