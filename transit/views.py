from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.maps.google import GoogleZoom
from django.contrib.gis.measure import D as distance

import urllib2,urllib,simplejson
from xml.etree import ElementTree as ET
import time

from homeland.forms import SearchForm
from transit.models import TransitStop, BusStop, BusLine

trimet_appid = "8DB644071B69C6C564921EE46"
trimet_arrivals_url = "http://developer.trimet.org/ws/V1/arrivals?appID=%s&" % trimet_appid

def get_nearby_stops(request):
    if request.GET.get('coords', ''):
        form = SearchForm(request.GET)
        if form.is_valid():
            (lat,lon) = form.cleaned_data['coords'].split(',')
            search_point = Point(float(lat),float(lon))
            stops = BusStop.objects.distance(search_point).filter(geom__distance_lte=(search_point, distance(mi=.5))).order_by('distance')
            routes={}
            nearby_stops=[]
            for stop in stops:
                if not routes.has_key("%s_%s" % (stop.route, stop.dir)):
                    routes["%s_%s" % (stop.route, stop.dir)]=True
                    nearby_stops.append(stop)
            return render_to_response('_transit_get_stops.html', {
                    'stops': nearby_stops
                })

    else:
        form = SearchForm()
        return render_to_response('search.html', {
                'form': form,
                })

def get_stop(request, stop_id):
    stop = TransitStop.objects.get(stop_id=stop_id)

    query_args = urllib.urlencode({ 'locIDs': stop.stop_id })
    response = urllib2.urlopen(trimet_arrivals_url + query_args)
    response_data = ET.XML(response.read())
    arrival_data = [element.attrib for element in response_data[1:]]

    arrivals=[]
    for arrival in arrival_data:
        try:
            arrivals.append({'route': arrival.get('route'), 
                             'sign': arrival.get('fullSign'),
                             'arrival_time': 
                             time.strftime("%H:%M %p", time.localtime(float(arrival.get('estimated'))/1000))})
        except:
            arrivals.append({'route': arrival.get('route'), 
                             'sign': arrival.get('fullSign'),
                             'arrival_time': time.strftime("%H:%M %p", 
                                                           time.localtime(float(arrival.get('scheduled'))/1000))})

    return render_to_response('_transit_stop.html', {
            'stop': stop,
            'arrivals': arrivals,
            'response': str(arrival_data),
            'url': trimet_arrivals_url + query_args
            })
