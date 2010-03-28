import os
from django.contrib.gis.utils import LayerMapping
from models import Neighborhood

neighborhood_mapping = {
    'name' : 'NAME',
    'poly' : 'POLYGON',
}
source_srs=102726
shapefile='data/shapefiles/neighborhoods_pdx030810.shp'
neighborhood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), shapefile))

def run(verbose=True):
    lm = LayerMapping(Neighborhood, neighborhood_shp, neighborhood_mapping,
                      transform=True, encoding='iso-8859-1', source_srs=source_srs)

    lm.save(strict=True, verbose=verbose)
