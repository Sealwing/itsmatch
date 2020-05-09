from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .api_processor import humans_get_all, humans_create, humans_get_details, humans_update_details, \
    humans_delete_details


# Create your views here.

# csrf_exempt for demonstration purposes
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def humans(request):
    """
    Method works with HTTP-methods GET and POST
    On GET returns list of humans from DB
        max list length is set in django settings
    On POST creates new human entry in DB
        as the correct info is provided
    """
    if request.method == 'GET':
        status, json_response, links = humans_get_all(request.GET)
        response = JsonResponse(json_response, status=status)
        if links is not None:
            response['Links'] = links
        return response
    elif request.method == 'POST':
        status, json_response = humans_create(request.POST, request.FILES)
        return JsonResponse(json_response, status=status)
    else:
        return HttpResponse(status=405)


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def humans_details(request, id):
    """
    Method works with HTTP-methods GET, PUT, DELETE
    On GET returns info about human with provided id
    On PUT updates DB human entry by id
    On DELETE removes DB human entry by id

    Arguments:
    id -- integer representing human id
    """
    if request.method == 'GET':
        status, details = humans_get_details(id)
        return JsonResponse(details, status=status)
    elif request.method == 'PUT':
        status, details = humans_update_details(id, request.GET)
        return JsonResponse(details, status=status)
    elif request.method == 'DELETE':
        status, details = humans_delete_details(id)
        return JsonResponse(details, status=status)
    else:
        return HttpResponse(status=405)
