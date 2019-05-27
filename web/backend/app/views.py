# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import GPIO
from .models import item
from .models import joke
from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def detail_json(request, GPIO_Pin):
    try:
        gpio = GPIO.objects.get(GPIO_Pin=GPIO_Pin)
        data = {
            "GPIO_Pin": gpio.GPIO_Pin,
            "toggle_on": gpio.toggle_on,
            "pub_date": gpio.pub_date
        }
    except GPIO.DoesNotExist:
        raise Http404("GPIO setting does not exist for pin %s" %GPIO_Pin)
    return JsonResponse(data)
def index_json(request):
    gpio_pins = GPIO.objects.all()
    data = {}
    ind = 1
    for gpio in gpio_pins:
        data[ind] = {}
        data[ind]["GPIO_Pin"] = gpio.GPIO_Pin
        data[ind]["toggle_on"] = gpio.toggle_on
        ind+=1
    return JsonResponse(data)
def detail(request, GPIO_Pin):
    try:
        gpio = GPIO.objects.get(GPIO_Pin=GPIO_Pin)
    except GPIO.DoesNotExist:
        raise Http404("GPIO setting does not exist for pin %s" %GPIO_Pin)
    return render(request, 'gpios/detail.html', {'gpio': gpio})
def index(request):
    gpio_pins = GPIO.objects.all()
    context = {
        'gpio_pin_settings': gpio_pins,
    }
    return render(request, 'gpios/index.html', context)
@csrf_exempt
def toggle(request,GPIO_Pin):
    if request.method == 'POST':
        if request.is_ajax():
            print("is ajax")
            gpio = GPIO.objects.filter(GPIO_Pin=GPIO_Pin)[0]
            print(gpio.toggle_on,not gpio.toggle_on)
            gpio.toggle_on = not gpio.toggle_on
            gpio.save()
            print("changed toggle to ",end='')
            print(gpio.toggle_on)
    
    return  HttpResponse()


    

