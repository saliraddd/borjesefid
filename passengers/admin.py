from django.contrib import admin
from .models import Passenger

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_id', 'phone_number', 'date_of_birth')
    list_filter = ('date_of_birth', 'created_at')
    search_fields = ('first_name', 'last_name', 'national_id', 'passport_number')
    readonly_fields = ('created_at', 'updated_at')
