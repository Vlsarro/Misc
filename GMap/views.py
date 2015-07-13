from urllib2 import URLError

from django.shortcuts import render
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.template import RequestContext

from geopy.geocoders.google import Google
from geopy.geocoders.google import GQueryError

from gmap import forms
from gmap import models


def geocode_address(address):
	address = address.encode('utf-8')
	geocoder = Google()
	try:
		_, latlon = geocoder.geocode(address)
	except (URLError, GQueryError, ValueError):
		return None
	else:
		return latlon
