from django.contrib.gis.db import models



class TransitStop(models.Model):
    "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,location_type"

    stop_id = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    stop_desc = models.CharField(max_length=400)
    zone_id = models.IntegerField()
    point = models.PointField(srid=4326)#, geography=True) 
    objects = models.GeoManager()

    def __unicode__(self):
        return self.stop_name

