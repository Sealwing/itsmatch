from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def matches(request):
    return JsonResponse({'status_code': '200',
                         'objects': ['gi', 'gi']})