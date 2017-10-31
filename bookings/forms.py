from django import forms

from .models import Reservation

class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['email', 'date','start_time', 'end_time'] 
		labels = {
			'email': 'Your Email Address', 
			'date': 'Reservation Date',
			'start_time': 'Start Time',
			'end_time': 'End Time',
			}