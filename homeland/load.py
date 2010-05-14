import os
from django.contrib.gis.utils import LayerMapping
from django.template.defaultfilters import slugify
from models import Neighborhood
import re
import simplejson
import urllib2,urllib
from googlemaps import GoogleMaps
from homeland.views import api_key

def get_locals():
    things = ['yoga', 'pole dancing', 'coffee shop', 'brew pub']

    gmaps = GoogleMaps(api_key)

    local = gmaps.local_search('brew pub near portland, or', numresults=GoogleMaps.MAX_LOCAL_RESULTS)
    for result in local['responseData']['results']:
        print result['titleNoFormatting']
        print result['streetAddress']
        print (result['lat'], result['lng'])


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
