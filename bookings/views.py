from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import stripe

from .forms import ReservationForm
from .models import Reservation, Payment

from pb_config.settings import STRIPE_TEST_SECRET_KEY

stripe.api_key = STRIPE_TEST_SECRET_KEY

# Create your views here.
def reservation(request):
	""" Show the reservation form and add a new reservation"""
	if request.method == 'POST':
		# Form was submitted
		form = ReservationForm(request.POST)
		if form.is_valid():
			# Form fields passed validation.
			form.save()
			new_reservation = form.save()
			# clean data?
			#... send email
			# save fee here
			Reservation().derive_quote_amount(new_reservation)
			return HttpResponseRedirect(reverse('bookings:payment',
				args=[new_reservation.id]))
			# Send to relevant payment.html
	else:
		form = ReservationForm()

	context = {
		'form': form,
		}
	return render(request, 'bookings/reservation.html', context)

@csrf_exempt
def payment(request, reservation_id):
	""" User's reservation data, agreement, payment. """
	reservation = Reservation.objects.get(id=reservation_id)
	context = {'reservation': reservation,}

	if request.method == "POST":
		# Payment form submitted. Process payment.

		token = request.POST.get("stripeToken")
		Payment().charge_card(token, reservation)

		return HttpResponseRedirect(reverse('bookings:confirmation',
			args=[reservation_id]))

	return render(request, 'bookings/payment.html', context)

def confirmation(request, reservation_id):
	""" Respond with booking confirmation data. """
	reservation = Reservation.objects.get(id=reservation_id)

	context = {
		'reservation': reservation
		}
	return render(request, 'bookings/confirmation.html', context)
		













