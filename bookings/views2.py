from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Booking, BookingPassenger
from flights.models import Flight
from passengers.models import Passenger

class UserBookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        return Booking.objects.all().select_related('flight')


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'
    context_object_name = 'booking'


def create_booking(request, pk):
    flight = get_object_or_404(Flight, id=pk)
    
    if request.method == 'POST':
        number_of_passengers = 1
        
        if number_of_passengers > flight.available_seats:
            return render(request, 'error.html', 
                         {'error': 'صندلی‌های کافی در دسترس نیست'})
        
        total_price = flight.price_per_seat * number_of_passengers
        
        booking = Booking.objects.create(
            flight=flight,
            total_price=total_price
        )
        
        return redirect('bookings:booking_detail', pk=booking.id)
    
    context = {
        'flight': flight,
        'num_passengers': 1,
        'total_price': flight.price_per_seat
    }
    return render(request, 'create_booking.html', context)

