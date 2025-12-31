from django.views.generic import ListView, DetailView, TemplateView
from .sepehr_api import get_sepehr_flights
from .models import Flight
from common.models import City
from django.shortcuts import render
from datetime import datetime


class LandingView(TemplateView):
    template_name = 'landing.html'
class LandingView2(TemplateView):
    template_name = 'landing2.html'
class LandingView3(TemplateView):
    template_name = 'landing3.html'


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all().order_by('name')
        context['total_flights'] = Flight.objects.filter(status='active').count()
        context['latest_flights'] = Flight.objects.filter(status='active')[:5]
        return context
    
class FlightListView(ListView):
    template_name = 'flights/flights_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        flights = []

        # پارامترهای جستجو از فرم
        origin_code = self.request.GET.get('origin')  # مثلاً THR
        destination_code = self.request.GET.get('destination')  # مثلاً MHD
        departure_date_str = self.request.GET.get('departure_date')  # مثلاً 2025-12-31

        # فیلتر پروازهای داخلی از دیتابیس خودمون
        db_flights = Flight.objects.select_related('airline', 'origin', 'destination')

        if origin_code:
            db_flights = db_flights.filter(origin__iata_code__iexact=origin_code)
        if destination_code:
            db_flights = db_flights.filter(destination__iata_code__iexact=destination_code)
        if departure_date_str:
            try:
                departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
                db_flights = db_flights.filter(departure_time__date=departure_date)
            except ValueError:
                pass  # اگر تاریخ نامعتبر بود، نادیده بگیر

        db_flights = db_flights.order_by('departure_time')

        for flight in db_flights:
            flights.append({
                'id': flight.id,
                'origin_city': flight.origin.name,
                'destination_city': flight.destination.name,
                'departure_time': flight.departure_time.strftime('%Y-%m-%d %H:%M'),
                'arrival_time': flight.arrival_time.strftime('%Y-%m-%d %H:%M'),
                'flight_number': flight.flight_number,
                'airline': flight.airline.name if flight.airline else 'نامشخص',
                'airline_name_en': flight.airline.name_en if flight.airline else '',
                'airline_iata': flight.airline.iata_code if flight.airline else '',
                'airline_logo': flight.airline.logo.url if flight.airline and flight.airline.logo else None,
                'aircraft_type': flight.aircraft_type or 'نامشخص',
                'price_per_seat': int(flight.price_per_seat),
                'available_seats': flight.available_seats,
                'source': 'internal',
                'is_internal': True,
            })

        # اگر بخوای بعداً پروازهای سپهر رو هم اضافه کنی، اینجا اضافه می‌شه

        return flights

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_passengers'] = int(self.request.GET.get('total_passengers', 1))
        # برای نمایش دوباره در فرم جستجو (اگر لازم بود)
        context['search_origin'] = self.request.GET.get('origin', '')
        context['search_destination'] = self.request.GET.get('destination', '')
        context['search_departure_date'] = self.request.GET.get('departure_date', '')
        return context

class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'


def test_view(request):
    return render(request, 'test.html')

