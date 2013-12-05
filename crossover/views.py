from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from crossover.models import Tweet

def index(request):
  context = {'tweets':Tweet.objects.all()}
  return render(request, 'crossover/index.html', context)

def data(request):
  data = serializers.serialize('json', Tweet.objects.all())
  return HttpResponse(data, content_type='application/json')
