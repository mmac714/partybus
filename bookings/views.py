from django.shortcuts import render

from .forms import ReservationForm

# Create your views here.
def reservation(request):
	""" Show the reservation form """
	if request.method == 'POST':
		# Form was submitted
		form = ReservationForm(request.POST)
		if form.is_valid():
			# Form fields passed validation.
			form.save()
			# clean data?
			#... send email
	else:
		form = ReservationForm()

	context = {
		'form': form,
		}
	return render(request, 'bookings/reservation.html', context)