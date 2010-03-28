from django.contrib.gis.db import models

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name
