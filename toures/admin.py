from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'tour_type', 'departure_date', 'price_per_person']
    list_filter = ['tour_type', 'departure_date']
    search_fields = ['title', 'destination']
    prepopulated_fields = {'slug': ('title',)}
    
