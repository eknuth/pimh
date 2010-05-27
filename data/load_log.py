from homeland.models import Request
import time
from django.contrib.gis.geos import Point

f = open("data/all.txt")

for line in f.readlines():
    (ts, url) = line.split()
    (lat,lon) = url.split("=")[1].split("%2C")


    date_time = time.strptime(ts, "%d/%b/%Y:%H:%M:%S")
    if url.startswith("/lookup"):
        r = Request(place_type="neighborhood", ts=date_time, point='POINT(%s %s)' % (lat, lon))
        r.save()
    else:
        place_type = url.split("?")[0].split("/")[2]
        r = Request(place_type=place_type, ts=date_time, point='POINT(%s %s)' % (lat, lon))
        r.save()
    print "saved ", url
