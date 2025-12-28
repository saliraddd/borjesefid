from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('cancelled', 'لغو شده'),
    ]
    
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=100)
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft_type = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-departure_time']
    
    def __str__(self):
        return f"{self.flight_number} - {self.origin_city} تا {self.destination_city}"
