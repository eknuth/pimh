from django.http import HttpResponse
from django.shortcuts import render_to_response



def district(request):
    return render_to_response('homeland.html')

