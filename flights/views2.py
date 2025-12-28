from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Flight

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_flights'] = Flight.objects.filter(status='active').count()
        context['latest_flights'] = Flight.objects.filter(status='active')[:5]
        return context


class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flights_list.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Flight.objects.filter(status='active')
        
        origin = self.request.GET.get('origin')
        destination = self.request.GET.get('destination')
        
        if origin:
            queryset = queryset.filter(origin_city__icontains=origin)
        if destination:
            queryset = queryset.filter(destination_city__icontains=destination)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # تعداد مسافران از صفحه جستجو
        context['adults'] = int(self.request.GET.get('adults', 1))
        context['children'] = int(self.request.GET.get('children', 0))
        context['infants'] = int(self.request.GET.get('infants', 0))
        context['total_passengers'] = context['adults'] + context['children'] + context['infants']
        return context


class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'


def test_view(request):
    return render(request, 'test.html')





# کلاس جدید برای لیست پروازها از API سپهر

class FlightListView(ListView):
    template_name = 'flights/flights_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # پارامترها از فرم جستجو
        origin = self.request.GET.get('origin', 'THR')
        destination = self.request.GET.get('destination', 'MHD')
        departure_date = self.request.GET.get('departure_date')

        if not departure_date:
            return []

        # فراخوانی API سپهر
        flights = get_sepehr_flights(origin, destination, departure_date)

        # اضافه کردن id موقت برای {% url 'flights:flight_detail' flight.id %}
        for i, flight in enumerate(flights, 1):
            flight['id'] = i  # id موقت

        return flights

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_passengers'] = int(self.request.GET.get('total_passengers', 1))
        return context

