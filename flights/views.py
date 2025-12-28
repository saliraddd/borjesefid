from django.views.generic import ListView, DetailView, TemplateView
from .sepehr_api import get_sepehr_flights
from .models import Flight
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
        context['total_flights'] = Flight.objects.filter(status='active').count()
        context['latest_flights'] = Flight.objects.filter(status='active')[:5]
        return context
    

class FlightListView(ListView):
    template_name = 'flights/flights_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # پارامترها از فرم جستجو
        origin = self.request.GET.get('origin', 'THR')
        destination = self.request.GET.get('destination', 'MHD')
        departure_date = self.request.GET.get('departure_date')

        flights = []

        if departure_date:
            # ۱. اول پروازهای دیتابیس خودمان (اولویت بالاتر)
            db_flights = Flight.objects.filter(
                origin_city__icontains=origin,
                destination_city__icontains=destination,
                departure_time__date=departure_date,
                status='active'
            ).order_by('departure_time')

            for flight in db_flights:
                flights.append({
                    'id': flight.id,
                    'origin_city': flight.origin_city,
                    'destination_city': flight.destination_city,
                    'departure_time': flight.departure_time.strftime('%Y-%m-%d %H:%M'),
                    'arrival_time': flight.arrival_time.strftime('%Y-%m-%d %H:%M'),
                    'flight_number': flight.flight_number,
                    'airline': flight.airline,
                    'aircraft_type': flight.aircraft_type,
                    'price_per_seat': int(flight.price_per_seat),
                    'available_seats': flight.available_seats,
                    'source': 'internal',  # برای تشخیص در template
                    'is_internal': True,
                })

            # ۲. بعد پروازهای سپهر ۳۶۰
            sepehr_flights = get_sepehr_flights(origin, destination, departure_date)
            for flight in sepehr_flights:
                flight['source'] = 'sepehr360'
                flight['is_internal'] = False
                flights.append(flight)

        return flights

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_passengers'] = int(self.request.GET.get('total_passengers', 1))
        context['origin'] = self.request.GET.get('origin', '')
        context['destination'] = self.request.GET.get('destination', '')
        context['departure_date'] = self.request.GET.get('departure_date', '')
        return context
    

class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'


def test_view(request):
    return render(request, 'test.html')

