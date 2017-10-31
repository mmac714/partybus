from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#from .reservation_num_generator import reservation_num_generator

# Create your models here.
class Reservation(models.Model):
	"""User entry reservation data.
	This is a one to many rationship. 
	Detail and payment will relate to this model."""
	email = models.EmailField()
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()

	def __str__(self):
		""" Return the id of the model """
		return str(self.id)

class Detail(models.Model):
	"""Additional details to be entered by the associate.
	This is a realtionship to the Reservation."""
	reservation = models.OneToOneField(
		Reservation,
			# creates a reservation_id column
		on_delete=models.CASCADE,
			#any objects related will be deleted.
		primary_key=True,
		)
	pick_up = models.TextField()
	drop_off = models.TextField()
	comments = models.TextField()
	# Not using charfield because postgres doesn't care
	# These values will not be entered by the customer
	# That will add some control.
	# Any second level reservation data should go here. 

	def __str__(self):
		""" Return the id of the model """
		return str(self.reservation_id)

