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




class FlightListView(ListView):
    template_name = 'flights/flights_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        origin = self.request.GET.get('origin', 'THR')
        destination = self.request.GET.get('destination', 'MHD')
        departure_date = self.request.GET.get('departure_date')
        flights = []
        # پروازهای داخلی (دیتابیس خودمون)
        db_flights = Flight.objects.select_related('airline').filter(
            origin__iata_code=origin,
            destination__iata_code=destination,
            departure_time__date=departure_date,
        ).order_by('departure_time')
        for flight in db_flights:
            flights.append({
                'id': flight.id,
                'origin_city': flight.origin.name if hasattr(flight, 'origin') else flight.origin_city,
                'destination_city': flight.destination.name if hasattr(flight, 'destination') else flight.destination_city,
                'departure_time': flight.departure_time.strftime('%Y-%m-%d %H:%M'),
                'arrival_time': flight.arrival_time.strftime('%Y-%m-%d %H:%M'),
                'flight_number': flight.flight_number,
                'airline': flight.airline.name if flight.airline else 'نامشخص',
                'airline_logo': flight.airline.logo.url if flight.airline and flight.airline.logo else None,
                'aircraft_type': flight.aircraft_type,
                'price_per_seat': int(flight.price_per_seat),
                'available_seats': flight.available_seats,
                'source': 'internal',
                'is_internal': True,
            })

        # پروازهای سپهر (اگر می‌خوای نگه داری)
        # sepehr_flights = get_sepehr_flights(...)
        # ...
        return flights
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_passengers'] = int(self.request.GET.get('total_passengers', 1))
        context['origin'] = self.request.GET.get('origin', '')
        context['destination'] = self.request.GET.get('destination', '')
        context['departure_date'] = self.request.GET.get('departure_date', '')
        return context
    


