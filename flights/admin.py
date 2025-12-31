from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'origin', 'destination', 'departure_time', 'available_seats', 'status')
    list_filter = ('status', 'airline', 'departure_time')
    search_fields = ('flight_number', 'airline', 'origin', 'destination')
    readonly_fields = ('created_at', 'updated_at')
