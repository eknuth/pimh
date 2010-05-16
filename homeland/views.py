from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from geopy import geocoders 
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.maps.google import GoogleZoom
from django.contrib.gis.measure import D as distance
import simplejson
import urllib2,urllib

from models import Neighborhood, Place
from forms import AddressForm, SearchForm


api_key='ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBQdkgRPlMVKT1vD1nTRJCRPuPWGKxT4RPVCd15nQW5msLk-f0ljd7C1Eg'
yelp_api_key='TyYPaW3bfrfJC4v0RIsiaQ'
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

def mobile(request):
    return render_to_response('mobile.html', {})


def browse_by_quad(request, quad):
    all_n = Neighborhood.objects.filter(quad=quad)
    
    return render_to_response('_browse.html', {
            'n': all_n,
            })


def browse_neighborhoods(request):
    all_n = Neighborhood.objects.all()
    gz = GoogleZoom()
    return render_to_response('map.html', {
            'n': all_n,
            'centroid': all_n.unionagg().centroid, 
            'key': api_key,
            'title': 'All Neighborhoods',
            'zoom': gz.get_zoom(all_n.unionagg())
            })

def lookup(request):
    if request.GET.get('coords', ''):
        form = SearchForm(request.GET)
        if form.is_valid():
            (lat,lon) = form.cleaned_data['coords'].split(',')
            n = get_neighborhood_by_point(Point(float(lat),float(lon)))
            search_response = {'name': n.name.title(), 'polygon': n.gpoly(), 
                               'slug': n.slug, 'wiki': n.wiki,
                               'centroid_x': "%.5f" % n.poly.centroid.x,
                               'centroid_y': "%.5f" % n.poly.centroid.y}
            return HttpResponse(simplejson.dumps(search_response),
                                    mimetype='application/json')

    else:
        form = SearchForm()
        return render_to_response('search.html', {
                'form': form,
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
    gz = GoogleZoom()
    return render_to_response('map.html', {
            'n': surrounding_n,
            'centroid_x': surrounding_n.unionagg().centroid, 
            'key': api_key,
            'title': n.name,
            'zoom': gz.get_zoom(surrounding_n.unionagg())
            })

def neighborhood(request, neighborhood_slug):
    n = Neighborhood.objects.get(slug=neighborhood_slug)
    return render_to_response('_neighborhood.html', {
            'wiki': n.wiki,
            'name': n.name.title()
            })

def local_search(request, place_type):
    if request.GET.get('coords', ''):
        form = SearchForm(request.GET)
        if form.is_valid():
            (lat,lon) = form.cleaned_data['coords'].split(',')
            search_point = Point(float(lat),float(lon))
            places = Place.objects.distance(search_point).filter(place_type=place_type).filter(point__distance_lte=(search_point, distance(mi=2))).order_by('distance')
            return render_to_response('_local_search.html', {
                    'title': place_type,
                    'places': places
                })

    else:
        form = SearchForm()
        return render_to_response('search.html', {
                'form': form,
                })
    
def place(request, place_id):
    p = Place.objects.get(id=place_id)
    return render_to_response('_place.html', {
            'place': p,
            })
