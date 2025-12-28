from django.contrib import admin
from .models import Booking, BookingPassenger

class BookingPassengerInline(admin.TabularInline):
    model = BookingPassenger
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'user', 'flight', 'number_of_passengers', 'total_price', 'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'flight')
    search_fields = ('booking_code', 'user__username')
    readonly_fields = ('booking_code', 'created_at', 'updated_at')
    inlines = [BookingPassengerInline]

@admin.register(BookingPassenger)
class BookingPassengerAdmin(admin.ModelAdmin):
    list_display = ('booking', 'passenger', 'seat_number')
    list_filter = ('booking__status',)
    search_fields = ('booking__booking_code', 'passenger__first_name')
