# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import GPIO
from .models import trained_version
from .models import generated_joke
# Register your models here.
admin.site.register(GPIO)
admin.site.register(trained_version)
admin.site.register(generated_joke)
