from models import Neighborhood
from django.contrib.gis import admin


admin.site.register(Neighborhood, admin.OSMGeoAdmin)
