from django.contrib import admin
from .models import Payment

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'booking', 'amount', 'payment_method', 'status', 'payment_date')
#     list_filter = ('status', 'payment_method', 'payment_date')
#     search_fields = ('booking__booking_code', 'transaction_id')
#     readonly_fields = ('transaction_id', 'created_at', 'updated_at')

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'amount', 'status', 'created_at', 'ref_id']  # payment_date رو با created_at جایگزین کن
    list_filter = ['status', 'created_at']  # payment_date رو حذف یا با created_at جایگزین کن
    search_fields = ['booking__booking_code', 'ref_id']
    readonly_fields = ['created_at', 'updated_at']


