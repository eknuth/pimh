from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.contrib.gis.maps.google.overlays import GPolygon


class Place(models.Model):
    name = models.CharField(max_length=400)
    place_type = models.CharField(max_length=40)
    address = models.CharField(max_length=400)
    static_map = models.URLField()
    point = models.PointField(srid=4326)#, geography=True) 
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    quad = models.CharField(max_length=2, null=True)
    slug = models.CharField(max_length=50)
    wiki = models.CharField(max_length=100, null=True)
    poly = models.PolygonField(srid=4326)#, geography=True) 
    objects = models.GeoManager()

    def gpoly(self):
        gpoly = GPolygon(self.poly)
        return gpoly.points.replace('GLatLng', 'google.maps.LatLng')


    def _get_slug(self):
        return slugify( self.name )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self._get_slug()
        super(Neighborhood, self).save(*args, **kwargs)

class Request(models.Model):
    place_type = models.CharField(max_length=40)
    ts = models.DateTimeField(auto_now=True)
    user_agent =  models.CharField(max_length=200)
    point = models.PointField(srid=4326)#, geography=True) 
    objects = models.GeoManager()

