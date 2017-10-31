"""Defines URL patterns for bookings."""

from django.conf.urls import url

from . import views

urlpatterns = [
	# Home page
	url(r'^$', views.reservation, name='reservation'),
]