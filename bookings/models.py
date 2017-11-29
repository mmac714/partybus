from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

import datetime, time

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
	stripe_customer_id = models.CharField(max_length=30, blank=True)

	def __str__(self):
		""" Return the id of the model """
		return str(self.reservation_id)

	def store_stripe_customer_in_db(self, reservation_instance, 
		customer_instance):
		""" takes the reservation number to store the stripe
		customer id and email. """
		res = reservation_instance
		customer = customer_instance

		# store variables
		res.stripe_customer_id = customer.id
		res.email = customer.email

		res.save()


	def create_stripe_customer(self, token, email, reservation):
		""" Creates a stripe customer.
		Saves the card on file.
		Save the customer's id and email to the database."""
		reservation = Payment(str(reservation))

		try:
			customer = stripe.Customer.create(
				source=token,
				email=email,
				)

		except stripe.error.CustomerError as ce:
			return ce

		else:
			Payment().store_stripe_customer_in_db(reservation, customer)

	def store_stripe_payment_in_db(self, reservation_instance, 
		charge_instance, customer_instance):
		""" store stripe objects to the payment instance """
		res = reservation_instance
		charge = charge_instance
		customer = customer_instance

		res.stripe_id = charge.id
		res.charge_amount = charge.amount
		res.charge_status = charge.outcome.type
		res.charge_desription = charge.description

		res.stripe_customer_id = customer.id
		res.email = customer.email

		res.save()

	def create_and_charge_customer(self, token, email, reservation):
		""" Creates a new customer and charges their card for
		the reservation. """
		fee = reservation.quote_amount
		reservation = Payment(str(reservation))

		try:
			customer = stripe.Customer.create(
				source=token,
				email=email,
				)

		except stripe.error.CustomerError as ce:
			return ce

		stripe_customer_id = customer.id

		try:
			charge = stripe.Charge.create(
				amount=fee,
				currency="usd",
				customer=stripe_customer_id,
				description="16-person party bus",
				)

		except stripe.error.CardError as ce:
			# Errors will only happen on fraud cards
			err = ce.json_body.get('error', {})
			new_payment.charge_status = err.get('type')
			new_payment.charge_desription = err.get('message')
			new_payment.save()
			return False

		else:
			Payment().store_stripe_payment_in_db(reservation, charge, customer)


	def send_booking_confirmation_email(self, email, reservation):
		""" send email to confirm reservation and payment. """
		payment = Payment.objects.get(reservation=reservation)
		email = [str(email),]
		fee = str(int(payment.charge_amount)/100)
		fee = "$" + fee + "0"
		charge_description = payment.charge_desription
		
		# set additional variables
		today = datetime.date.today()
		subject = 'Thanks for booking with us!'
		body = get_template('bookings/confirmation_email.html').render(
			{
			'email': email,
			'fee': fee,
			'today':today, 
			'charge_description':charge_description
			})
		sender = 'operations@partybus.com'
		recipient = email

		send_mail(subject, "", sender, recipient, html_message=body, fail_silently=False)