from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'کارت اعتباری'),
        ('debit_card', 'کارت بانکی'),
        ('bank_transfer', 'انتقال بانکی'),
        ('online_wallet', 'کیف پول الکترونیکی'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('refunded', 'بازگرداندی'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.PositiveBigIntegerField(help_text="مبلغ به ریال")
    authority = models.CharField(max_length=100, blank=True, null=True)
    ref_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, default='online_wallet')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"پرداخت رزرو {self.booking.booking_code} - {self.amount:,} ریال"
