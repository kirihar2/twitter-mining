# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import GPIO
from .models import trained_version
from .models import generated_joke
from django.shortcuts import render
from django.core import serializers
from django.http import Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from dadjokegen import generate,train,updateCurrentModelFilename,getLatestVersionNumber
from datetime import datetime

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


def get_versions(request):
    data = {}
    data['versions'] = []
    if request.method == 'GET':
        data['versions'] = serializers.serialize('json',trained_version.objects.all())
    return JsonResponse(data)

def get_version(request,version):
    data = {}
    data['version'] = {}
    if request.method == 'GET':
        version = trained_version.objects.get(version=version)
        data['version'] = _serialize_version(version)
    return JsonResponse(data)
def _serialize_version(version):
    return {
            'version': version.version,
            'filename': version.filename,
            'extension': version.extension
    }
@csrf_exempt
def create_version(request):
    data = {}
    data['version'] = {}
    version = int(request.headers.get('version'))
    epochs = int(request.headers.get('epochs'))
    tweetcount = int(request.headers.get('tweetcount'))
    if request.method == 'POST':
        if version == None: 
            version = 0
        if len(trained_version.objects.filter(version=version)) > 0: #TODO filter by filename when added to input as well
            print("Trained version %s exists, creating new trained version file.",str(version))
            weight_filename = 'weights/textgenrnn_weights'
            unassigned_version = getLatestVersionNumber(weight_filename)
            created_filename = train(epochs=epochs,tweet_count=tweetcount,output_filename=weight_filename)
            created_version = trained_version.create(version=unassigned_version,filename=created_filename)
            data['version'] = _serialize_version(created_version)
    return JsonResponse(data)
def create_jokes(request,count,version):
    data={}
    data['jokes'] = {}
    if request.method == 'POST':
        if request.is_ajax():
            
            jokes = generate(version,count)
            create_datetime = datetime.now()
            for ind in len(jokes):
                joke = jokes[ind]
                ret = generated_joke.create(joke.text,version,create_datetime)
                data['jokes'][ind] = serializers.serialize('json',ret)
                ret.save()

    return JsonResponse(data)

def get_jokes(request):
    if request.method == 'GET':
        data={}
        data['jokes'] = serializers.serialize('json',generated_joke.objects.all())
    return JsonResponse(data)

