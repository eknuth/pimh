import os
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point
from django.template.defaultfilters import slugify

import re
import simplejson
import urllib2,urllib
from googlemaps import GoogleMaps

from homeland.views import api_key
from homeland.models import Neighborhood, Place
from transit.models import TransitStop

def load_stops():
    "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,location_type"
    f = open("transit/data/stops.txt")
    header=f.readline()
    for stop in f.readlines():
        items = stop.split(',')
        stop_id = items[0]
        stop_name = items[2]
        stop_desc = items[3]
        stop_lat = items[4]
        stop_lon = items[5]
        zone_id = items[6]
        ts = TransitStop(stop_id=stop_id, stop_name=stop_name, stop_desc=stop_desc, zone_id=zone_id,
                         point=Point(float(stop_lon), float(stop_lat)))
        ts.save()
        print "Saved %s" % ts.stop_name
                        
                         
        
