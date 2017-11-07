from django.conf import settings
import stripe

stripe.api_key = "sk_test_pN7XZ5JeWtIlU4uAWAnBaXX9"


# Step 1: Card information is entered
stripe.Token.create(
  card={
    "number": '4242424242424242',
    "exp_month": 12,
    "exp_year": 2018,
    "cvc": '123'
  },
)

# ^^ step 1 is created by the form

# Step 2: Token received 
# put token in source

stripe.Charge.create(
  amount=1500,
  currency="usd",
  source="tok_1BJr2kGbnnaXpMDuxekMRWhZ", 
  description='Reservation.id',
)

# step 3: retrieve charge put charge info into Payment data
# charg ID will be the first argument in retrieve

stripe.Charge.retrieve(
  "ch_1BKI3fGbnnaXpMDuCaUhKLW4",
  api_key="sk_test_pN7XZ5JeWtIlU4uAWAnBaXX9"
)

4242 4242 4242 4242

"""
How does checkout.js create the token?

How do I retrieve that token?

  """
    if 'reservationform' in request.method == "POST":
    # reservation form was submitted
      r_form = ReservationForm(request.POST, prefix='reservation')
      if r_form.is_valid():
        r_form.save()
      d_form = DetailForm(prefix='detail')

    elif 'detailform' in request.POST:  
    # detail form was submitted
      d_form = DetailForm(request.POST, prefix='detail')
      if d_form.is_valid():
        d_form.save()
      r_form = ReservationForm(prefix='reservation')

  else:
    r_form = ReservationForm(prefix='reservationform',initial={
      'date': reservation.date})
    d_form = DetailForm(prefix='detailform')

  context = {
    'reservation': reservation,
    'r_form': r_form,
    'd_form': d_form,
    }
      """









