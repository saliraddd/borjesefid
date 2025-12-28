from flights.models import Flight
from datetime import datetime, timedelta

# ایجاد یک پرواز نمونه
flight = Flight.objects.create(
    flight_number='IR101',
    airline='ایران ایر',
    origin_city='تهران',
    destination_city='دبی',
    departure_time=datetime.now() + timedelta(days=3),
    arrival_time=datetime.now() + timedelta(days=3, hours=2),
    aircraft_type='Airbus A320',
    total_seats=180,
    available_seats=150,
    price_per_seat=2500000,
    status='active'
)

print(f"✅ پرواز {flight.flight_number} ایجاد شد")
