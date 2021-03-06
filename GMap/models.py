from urllib2 import URLError

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from geopy import geocoders


class kindergarten(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, null =True, blank=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = geocoders.Yandex()
            try:
                _, latlon = geocoder.geocode(address)
            except (URLError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = geos.fromstr(point)
            super(kindergarten, self).save()