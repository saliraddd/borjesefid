from django.db import models
from django.contrib.auth.models import User
from flights.models import Flight
from passengers.models import Passenger
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    booking_code = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.PositiveBigIntegerField(help_text="مبلغ کل به ریال")
    number_of_passengers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"رزرو {self.booking_code}"


class BookingPassenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('booking', 'passenger')
    
    def __str__(self):
        return f"{self.passenger} - صندلی {self.seat_number}"
    
