from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from geopy import geocoders 
from django.contrib.gis.geos import Point

from models import Neighborhood
from forms import AddressForm

api_key='ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBQdkgRPlMVKT1vD1nTRJCRPuPWGKxT4RPVCd15nQW5msLk-f0ljd7C1Eg'

def get_neighborhood_by_point(point):
    """
    Get Neighborhood by Point
    """
    return Neighborhood.objects.get(poly__intersects=point)
    
def get_neighborhood_by_address(address):
    """
    Get Neighborhood by Address

    #Tests
    >>> get_neighborhood_by_address('2728 SE 52nd Ave, Portland, OR')
    'South Tabor'
    """
    g = geocoders.Google(api_key)
    place, (lat, lon) = g.geocode(address)
    return get_neighborhood_by_point(Point(lon,lat))

def get_neighborhood(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AddressForm(request.POST)
        if form.is_valid():
            n = get_neighborhood_by_address(form.cleaned_data['address'])
            return HttpResponseRedirect('/neighborhood/%s' % n.slug)
    else:
        form = AddressForm()
        return render_to_response('homeland.html', {
                'form': form,
                })


def map_neighborhood(request, neighborhood_slug):
    n = Neighborhood.objects.get(slug=neighborhood_slug)
  
    return render_to_response('map.html', {
            'n': n,
            'key': api_key,
            })
