"""Defines URL patterns for bookings."""

from django.conf.urls import url

from . import views

urlpatterns = [
	# Home page
	url(r'^$', views.reservation, name='reservation'),
	url(r'^payment/(?P<reservation_id>\d+)/$', views.payment, name='payment'),
	url(r'^confirmation/(?P<reservation_id>\d+)/$', views.confirmation, 
		name='confirmation'),
	url(r'^booking/(?P<reservation_id>\d+)$',
		views.booking, name='booking'),
	url(r'^booking_list/$', views.booking_list, name='booking_list'),

]