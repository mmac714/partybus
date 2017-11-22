from django import forms
from .models import Reservation, Detail

import datetime

from pb_config.settings import DATE_INPUT_FORMATS

# find the next saturday for date initial value
today = datetime.date.today()
saturday = today + datetime.timedelta( (5-today.weekday()) % 7)


class ReservationForm(forms.ModelForm):
	date = forms.DateField(widget=forms.SelectDateWidget, 
		initial=saturday)
	duration = forms.IntegerField(widget=forms.NumberInput, min_value=3, label='# of hours')
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