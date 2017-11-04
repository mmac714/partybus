from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse

import stripe
import uuid

from pb_config.settings import STRIPE_TEST_SECRET_KEY

stripe.api_key = STRIPE_TEST_SECRET_KEY

#from .reservation_num_generator import reservation_num_generator

# Create your models here.
class Reservation(models.Model):
	"""User entry reservation data.
	This is a one to many rationship. 
	Detail and payment will relate to this model."""
	date = models.DateField()
	duration = models.IntegerField()
	quote_amount = models.IntegerField(default=0)

	def __str__(self):
		""" Return the id of the model """
		return str(self.id)

	def derive_quote_amount(self, reservation):
		""" Calculate and store the payment amount. """
		duration = reservation.duration
		rate = 10000
		reservation.quote_amount = duration * rate

		reservation.save()


class Detail(models.Model):
	"""Additional details to be entered by the associate.
	This is a realtionship to the Reservation."""
	reservation = models.OneToOneField(
		Reservation,
		on_delete=models.CASCADE,
		primary_key=True,
		)
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)
	location_pick_up = models.TextField(null=True, blank=True)
	location_drop_off = models.TextField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)
	# Not using charfield because postgres doesn't care
	# These values will not be entered by the customer
	# That will add some control.
	# Any second level reservation data should go here. 

	def __str__(self):
		""" Return the id of the model """
		return str(self.reservation_id)

class Payment(models.Model):

	reservation = models.OneToOneField(Reservation,
		primary_key=True,
		)
	email = models.EmailField()
	stripe_id = models.CharField(max_length=30, blank=True)
	paid = models.BooleanField(default=False)
	charge_amount = models.IntegerField(default=0)

	def __str__(self):
		""" Return the id of the model """
		return str(self.reservation_id)

	def check_if_already_paid(self):
		if self.paid: # don't let this be charged twice!
			return False, Exception(message="Already charged!")

	def charge_card(self, token, reservation):

		new_payment = Payment(str(reservation))
		fee = reservation.quote_amount

		if new_payment.paid: # don't let this be charged twice!
			return False, HttpResponse("Already charged!")

		try:
			charge = stripe.Charge.create(
				amount = fee,
				currency = "usd",
				source = token,
				description = "14 passenger bus"
				)

			new_payment.stripe_id = charge.id
			new_payment.email = charge.source.name
			new_payment.charge_amount = charge.amount

		except stripe.error.CardError as ce:
			return False, HttpResponse(ce)

		else:
			new_payment.paid = True
			new_payment.save()




