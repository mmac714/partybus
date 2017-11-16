from django.shortcuts import render, get_object_or_404, \
redirect, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import stripe

from .forms import ReservationForm, DetailForm, BookingResForm
from .models import Reservation, Detail, Payment

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
			# save fee here
			Reservation().create_detail_and_payment_instance(new_reservation)
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

		# Send email here...

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

@login_required
def booking(request, reservation_id):
	""" Page for associate to fill out Reservation detail. """
	reservation = Reservation.objects.get(id=reservation_id)
	detail = Detail.objects.get(reservation=reservation_id)
	payment = Payment.objects.get(reservation=reservation_id)

	if request.method == 'POST' and 'btn-r_form':
		r_form = BookingResForm(request.POST, instance=reservation)
		if r_form.is_valid():
			r_form.save()

			return HttpResponseRedirect(reverse('bookings:booking',
				args=[reservation_id]))

	if request.method == 'POST' and 'btn-d_form':
		d_form = DetailForm(request.POST, instance=detail)
		if d_form.is_valid():
			d_form.save()

			return HttpResponseRedirect(reverse('bookings:booking',
				args=[reservation_id]))

	else:
		r_form = BookingResForm(initial={
			'date': reservation.date,
			'duration': reservation.duration,
			'quote_amount': reservation.quote_amount,
			'happening':reservation.happening,
			})

		d_form = DetailForm(initial={
			'start_time': detail.start_time,
			'end_time': detail.end_time,
			'location_pick_up': detail.location_pick_up,
			'location_drop_off': detail.location_drop_off,
			'comments': detail.comments
			})

		context = {
    		'reservation': reservation,
    		'r_form': r_form,
    		'd_form': d_form,
    		'payment': payment
    		}

		return render(request, 'bookings/booking.html', context)

@login_required
def booking_list(request):
	""" Show all bookings. """
	bookings = Reservation.objects.order_by('date')
	detail = Detail()
	payment = Payment()

	context = {	
		'bookings': bookings,
		'detail': detail,
		'payment': payment,
		}
	return render(request, 'bookings/booking_list.html', context)
		
























