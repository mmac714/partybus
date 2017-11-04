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
  "ch_1BKHfjGbnnaXpMDuqcjOSbU7",
  api_key="sk_test_pN7XZ5JeWtIlU4uAWAnBaXX9"
)

"""
How does checkout.js create the token?

How do I retrieve that token?











