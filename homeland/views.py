from django.http import HttpResponse
from django.shortcuts import render_to_response
from geopy import geocoders 
from django.contrib.gis.geos import Point
from models import Neighborhood

api_key='ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBQdkgRPlMVKT1vD1nTRJCRPuPWGKxT4RPVCd15nQW5msLk-f0ljd7C1Eg'


def get_neighborhood_by_address(address):
    """
    Get Neighborhood by Address

    #Tests
    >>> get_neighborhood_by_address('2728 SE 52nd Ave, Portland, OR')
    'South Tabor'
    """
    g = geocoders.Google(api_key)
    place, (lat, lon) = g.geocode(address)
    pnt = Point(lon,lat)
    n = Neighborhood.objects.get(poly__intersects=pnt)
    return n

def neighborhood(request):
    return render_to_response('homeland.html')

