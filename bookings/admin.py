from django.contrib import admin

# Register your models here.
from .models import Reservation, Detail

admin.site.register(Reservation)
admin.site.register(Detail)