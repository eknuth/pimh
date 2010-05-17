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


class BusStop(models.Model):
    keyitem = models.CharField(max_length=4)
    rte = models.CharField(max_length=3)
    dir = models.FloatField()
    loc_id = models.IntegerField()
    location = models.CharField(max_length=40)
    jurisdic = models.CharField(max_length=14)
    zip = models.FloatField()
    route = models.CharField(max_length=50)
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()

busstop_mapping = {
    'keyitem' : 'KEYITEM',
    'rte' : 'RTE',
    'dir' : 'DIR',
    'loc_id' : 'LOC_ID',
    'location' : 'LOCATION',
    'jurisdic' : 'JURISDIC',
    'zip' : 'ZIP',
    'route' : 'ROUTE',
    'geom' : 'POINT',
}


class BusLine(models.Model):
    rte = models.CharField(max_length=3)
    dir = models.FloatField()
    keyitem = models.CharField(max_length=4)
    rte_desc = models.CharField(max_length=28)
    dir_desc = models.CharField(max_length=49)
    route = models.CharField(max_length=50)
    length = models.FloatField()
    geom = models.MultiLineStringField(srid=4326)
    objects = models.GeoManager()

busline_mapping = {
    'rte' : 'RTE',
    'dir' : 'DIR',
    'keyitem' : 'KEYITEM',
    'rte_desc' : 'RTE_DESC',
    'dir_desc' : 'DIR_DESC',
    'route' : 'ROUTE',
    'length' : 'LENGTH',
    'geom' : 'MULTILINESTRING',
}
