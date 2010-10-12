from django.db import models
from homeland.models import Neighborhood
from django.contrib.gis.geos import Point, Polygon, MultiPolygon

# Create your models here.

class DIY_Neighborhood(Neighborhood):
    user = models.CharField(max_length='100')
    
#    def create(self,poly_str):
#        print poly_str
#        points = poly_str.split(',')
#       for point in points:
#            print point
       
