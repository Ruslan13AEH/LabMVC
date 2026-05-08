from django.contrib import admin
from .models import Trip, Traveler, Reservation


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['destination', 'start_date', 'end_date', 'price', 'max_participants']
    search_fields = ['destination']
    list_filter = ['start_date']


@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone']
    search_fields = ['last_name', 'first_name', 'email']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['traveler', 'trip', 'status', 'created_at']
    list_filter = ['status']
