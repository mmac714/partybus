from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, reverse

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
	duration = models.IntegerField("Number of hours")
	quote_amount = models.IntegerField(default=0)
	happening = models.BooleanField(default=False)
	objects = models.Manager()


	def __str__(self):
		""" Return the id of the model """
		return str(self.id)

	def derive_quote_amount(self, reservation):
		""" Calculate and store the payment amount. """
		duration = reservation.duration
		rate = 15000
		reservation.quote_amount = duration * rate

		reservation.save()

	def create_detail_and_payment_instance(self, reservation):
		Detail.objects.create(reservation=reservation)
		Payment.objects.create(reservation=reservation)


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
	charge_amount = models.IntegerField(default=0)
	charge_status = models.CharField(max_length=100, blank=True)
	charge_desription = models.CharField(max_length=200, blank=True)

	def __str__(self):
		""" Return the id of the model """
		return str(self.reservation_id)

	def store_stripe_objects_in_db(self, reservation_instance, 
		charge_instance):
		""" store stripe objects to the payment instance """
		res = reservation_instance
		charge = charge_instance

		res.stripe_id = charge.id
		res.email = charge.source.name
		res.charge_amount = charge.amount
		res.charge_status = charge.outcome.type
		res.charge_desription = charge.outcome.seller_message

		res.save()

	def charge_card(self, token, reservation):
		""" uses the form token to charge the card, create a 
		charge or CardError object and stores the object data. """
		new_payment = Payment(str(reservation))
		fee = reservation.quote_amount

		if new_payment.charge_amount:
		# if paid=true, do not process payment and
		# send directly to confirmation page. 
			return HttpResponseRedirect(reverse('bookings:confirmation',
				args=[reservation]))

		try:
			charge = stripe.Charge.create(
						amount = fee,
						currency = "usd",
						source = token,
						description = str(reservation)
						)

		except stripe.error.CardError as ce:
			# an error object is created as the 
			# the result of a card error.
			# This error will happen on blocked (fraud) cards
			err = ce.json_body.get('error', {})
			new_payment.charge_status = err.get('type')
			new_payment.charge_desription = err.get('message')
			new_payment.save()
			return False
				# will forward them to confirm page with charge 
				# status and description

		else:
			Payment().store_stripe_objects_in_db(new_payment, charge)




