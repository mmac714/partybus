from django import forms

from .models import Reservation, Detail

class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['date','duration'] 
		labels = {
			'date': 'Reservation Date',
			'duration': 'Number of Hours',
			}

class DetailForm(forms.ModelForm):
	class Meta:
		model = Detail
		fields = [
			'start_time', 
			'end_time', 
			'location_pick_up',
			'location_drop_off', 
			'comments'
			]
		labels = {
			'start_time': 'Reservation Start Time',
			'end_time': 'Reservation End Time',
			'location_pick_up': 'Pick-up address',
			'location_drop_off': 'Drop-off address',
			'comments': 'comments and notes',
			}

class BookingResForm(forms.ModelForm):
	""" list all reservation objects """
	class Meta:
		model = Reservation
		fields = ['date','duration', 'quote_amount', 'happening'] 