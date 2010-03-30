from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.contrib.gis.maps.google.overlays import GPolygon

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    poly = models.PolygonField(srid=4326) 
    objects = models.GeoManager()

    def gpoly(self):
        return GPolygon(self.poly)

    def _get_slug(self):
        return slugify( self.name )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self._get_slug()
        super(Neighborhood, self).save(*args, **kwargs)
