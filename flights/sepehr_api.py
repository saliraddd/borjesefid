# flights/sepehr_api.py
import requests
from datetime import datetime
import jdatetime

def get_sepehr_flights(origin='THR', destination='MHD', departure_date='2025-12-25'):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://sepehr360.ir/",
        "Origin": "https://sepehr360.ir",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*"
    }

    # تبدیل تاریخ میلادی به شمسی برای API
    gregorian_date = datetime.strptime(departure_date, '%Y-%m-%d')
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    date_param = jalali_date.strftime("%Y-%m-%d")

    base_url = "https://api.sepehr360.ir/api/Parvaz/Oneway/B2c/Search/GetNatayejParvaz"

    payload = {
        "originAirportIataCode": origin.upper(),
        "destinationAirportIataCode": destination.upper(),
        "searchDate": date_param,
        "isMiladi": False,
        "sortOrder": 1,
        "pageNumber": 0,
    }

    try:
        response = session.post(base_url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("خطا در اتصال به سپهر ۳۶۰:", e)
        return []

    flights = []

    for radif in data.get('radifList', []):
        if not radif.get('radifParvazi'):
            continue

        parvaz = radif['radifParvazi']
        hour = parvaz['zamanKhorojAzMabda']
        class_flight = parvaz['cabinType']
        flight_number = parvaz['cleanFlightNumber']
        airline = parvaz['airlineNameFa']

        for item in parvaz.get('radifParvaziEntekhabForoshandeList', []):
            key = 'parvazCharteri' if item.get('parvazCharteri') else 'parvazWebservice' if item.get('parvazWebservice') else None
            if not key:
                continue

            info = item[key]
            try:
                price = int(info['formattedAdultPrice'].replace(',', ''))
                available_seats = int(info['seatCount'])
            except:
                continue

            flights.append({
                'origin_city': origin.upper(),
                'destination_city': destination.upper(),
                'departure_time': f"{departure_date} {hour}",
                'arrival_time': f"{departure_date} {hour}",  # تقریبی – بعداً دقیق می‌کنیم
                'flight_number': flight_number,
                'airline': airline,
                'aircraft_type': 'نامشخص',  # سپهر نداره
                'price_per_seat': price,
                'available_seats': available_seats,
                'class_type': class_flight,
                'source': 'sepehr360',
            })

    return flights