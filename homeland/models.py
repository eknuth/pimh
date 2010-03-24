from django.contrib.gis.db import models

class District(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField()
    objects = models.GeoManager()
