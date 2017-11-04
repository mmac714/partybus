from django import forms

from .models import Reservation

class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['date','duration'] 
		labels = {
			'date': 'Reservation Date',
			'duration': 'Number of Hours',
			}