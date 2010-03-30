from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from geopy import geocoders 
from django.contrib.gis.geos import Point, Polygon, MultiPolygon

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

def dissolve_neighborhoods(all_n):
    all_polygons = []

    for n in all_n:
        all_polygons.append(n.poly)
    return MultiPolygon(all_polygons)

def browse_neighborhoods(request):
    all_n = Neighborhood.objects.all()
    return render_to_response('map.html', {
            'n': all_n,
            'key': api_key,
            })

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
    surrounding_n = Neighborhood.objects.filter(poly__intersects=n.poly)
    dissolved_n = dissolve_neighborhoods(surrounding_n)
    return render_to_response('map.html', {
            'n': n, surrounding_n,
            'centroid': dissolved_n.centroid, 
            'key': api_key,
            })
