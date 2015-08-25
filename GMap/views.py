from urllib2 import URLError

from django.contrib.gis.geos import Point
from django.shortcuts import render_to_response
# from django.contrib.gis import geos
from django.contrib.gis import measure
from django.template import RequestContext

from geopy import geocoders

from GMap import forms, models


def geocode_address(address):

    address = address.encode('utf-8')
    geocoder = geocoders.Yandex()
    try:
        _, latlon = geocoder.geocode(address)
    except (URLError, ValueError):
        return None
    else:
        return latlon


def get_objects(longitude, latitude):

    # current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    current_point = Point(longitude, latitude)
    distance_from_point = {'km': 30}
    objects = models.kindergarten.gis.filter(location__distance_lte=(current_point,
                                            measure.D(**distance_from_point)))
    objects = objects.distance(current_point).order_by('distance')
    return objects.distance(current_point)


def home(request):
    form = forms.AddressForm()
    kindergartens = []
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                latitude, longitude = location
                kindergartens = get_objects(longitude, latitude)

    return render_to_response(
        'home.html',
        {'form': form, 'kindergartens': kindergartens},
        context_instance=RequestContext(request))

