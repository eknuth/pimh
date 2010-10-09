from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from geopy import geocoders 
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.maps.google import GoogleZoom
from django.contrib.gis.measure import D as distance
import simplejson
import urllib2,urllib

from settings import pimh_gmaps_api_key, portlandismyhomeland_gmaps_api_key, yelp_api_key
from settings import pimh_gmaps_api_key as api_key
from models import Neighborhood, Place, Request
from forms import AddressForm, SearchForm

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
    g = geocoders.Google(pimh_gmaps_api_key)
    place, (lat, lon) = g.geocode(address)
    return get_neighborhood_by_point(Point(lon,lat))



def dissolve_neighborhoods(all_n):
    all_polygons = []

    for n in all_n:
        all_polygons.append(n.poly)
    return MultiPolygon(all_polygons)

def browse(request, flag=False):
    if request.META.get("HTTP_HOST", '').endswith("pimh.info"):
        api_key=pimh_gmaps_api_key
    else:
        api_key = portlandismyhomeland_gmaps_api_key

    return render_to_response('mobile.html', {'google_api_key': api_key,
                                              'home_template': "_home.html",
                                              'referer': request.META.get("HTTP_HOST", '') })


def neighborhoods_by_quad(request, quad):
    all_n = Neighborhood.objects.filter(quad=quad).order_by('name')
    
    return render_to_response('_browse.html', {
            'all_n': all_n,
            'quad': quad,
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
            pnt=Point(float(lat),float(lon))
            n = get_neighborhood_by_point(pnt)
            r = Request(point=pnt, place_type="neighborhood")
            r.save()
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
    return render_to_response('_home.html', {
            'n': n,
            'quad': n.quad,
            })

def local_search(request, place_type):
    if request.GET.get('coords', ''):
        form = SearchForm(request.GET)
        if form.is_valid():
            (lat,lon) = form.cleaned_data['coords'].split(',')
            search_point = Point(float(lat),float(lon))
            r = Request(point=search_point, place_type=place_type)
            r.save()
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

def request_kml(request):
    all_r = Request.objects.all()
    return render_to_response('base.kml', {
            'points': all_r,
            },  mimetype="application/vnd.google-earth.kml+xml")

def map(request, place_type):
    points = Place.objects.filter(place_type=place_type)
    return render_to_response('map.html', {
            'points': points
            })

