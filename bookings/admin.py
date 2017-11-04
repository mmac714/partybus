from django.contrib import admin

# Register your models here.
from .models import Reservation, Detail, Payment

admin.site.register(Reservation)
admin.site.register(Detail)
admin.site.register(Payment)