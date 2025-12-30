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
