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

def get_places():
    place_types = {'yoga': 'yoga', 'pole': 'pole dancing', 'coffee':'coffee shop', 
              'beer': 'brew pub', 'strip': 'strip club', 'bikes': 'bicycle shop'}

    gmaps = GoogleMaps(api_key)
    for place_type in place_types:
        local = gmaps.local_search('%s near portland, or' % place_types[place_type], 
                                   numresults=GoogleMaps.MAX_LOCAL_RESULTS)
        for result in local['responseData']['results']:
            kwargs={'name': result['titleNoFormatting'].encode('utf-8'),
                    'address': result['streetAddress'].encode('utf-8')}
            try:
                p = Place.objects.get(**kwargs)
            except Place.DoesNotExist:
                p = Place(**dict((k,v) for (k,v) in kwargs.items() if '__' not in k))
            
            p.static_map=result['staticMapUrl'].encode('utf-8')
            p.point=Point(float(result['lng']), float(result['lat']))
            p.place_type=place_type
            p.save()
            print "saved %s" % p.name

def map_quads():
    quad = ""
    neighborhoods = {}
    f = open("data/wikipedia/wikipedia-neighborhoods.txt")
    for line in f:
        if line[0] == '-':
            quad=line[2:].rstrip()
        else:
            m = re.search('([\w, -.]+)\|([\w, -.]+)]', line)
            if m:
                try:
                    n = Neighborhood.objects.get(slug=slugify(m.group(2)))
                    n.quad=quad
                    n.wiki=m.group(1).replace(' ', '_')
                    n.save()
                    #neighborhoods[slugify(m.group(2))] = {'quad': quad, 'wiki': m.group(1).replace(' ', '_')}
                except:
                    print "Couldn't do %s" % m.group(2)

        
def load(verbose=True):
    neighborhood_mapping = {
        'name' : 'NAME',
        'poly' : 'POLYGON',
        }
    source_srs=102726
    shapefile='data/shapefiles/neighborhoods_pdx030810.shp'
    neighborhood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), shapefile))
    lm = LayerMapping(Neighborhood, neighborhood_shp, neighborhood_mapping,
                      transform=True, encoding='iso-8859-1', source_srs=source_srs)

    lm.save(strict=True, verbose=verbose)
