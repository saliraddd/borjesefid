from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView
from .models import Booking, BookingPassenger
from flights.models import Flight
from passengers.models import Passenger  # از اپ passengers ایمپورت کن


class UserBookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        # فقط رزروهای کاربر فعلی
        return Booking.objects.filter(user=self.request.user).select_related('flight').order_by('-booking_date')


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        # فقط رزروهای کاربر فعلی
        return Booking.objects.filter(user=self.request.user)


@login_required
def create_booking(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    
    # تعداد مسافران از صفحه جستجو (GET)
    adults = int(request.GET.get('adults', 1))
    children = int(request.GET.get('children', 0))
    infants = int(request.GET.get('infants', 0))
    total_passengers = adults + children + infants
    
    # محاسبه قیمت کل (فعلاً همه یک قیمت – بعداً تخفیف کودک اضافه کن)
    total_price = int(flight.price_per_seat) * total_passengers
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # چک ظرفیت
                if total_passengers > flight.available_seats:
                    messages.error(request, 'متأسفانه صندلی کافی برای این تعداد مسافر موجود نیست.')
                    return redirect('flights:flight_list')
                
                # ایجاد رزرو
                booking = Booking.objects.create(
                    user=request.user,
                    flight=flight,
                    total_price=total_price,
                    number_of_passengers=total_passengers,
                    status='pending'
                )
                
                # دریافت اطلاعات مسافران از فرم
                # first_names = request.POST.getlist('first_name')
                # last_names = request.POST.getlist('last_name')
                # national_ids = request.POST.getlist('national_id')
                # birth_dates = request.POST.getlist('birth_date')

                first_names = request.POST.getlist('first_name[]')
                last_names = request.POST.getlist('last_name[]')
                national_ids = request.POST.getlist('national_id[]')
                birth_dates = request.POST.getlist('birth_date[]')
                
                if len(first_names) != total_passengers:
                    messages.error(request, 'تعداد اطلاعات مسافران با تعداد انتخاب شده مطابقت ندارد.')
                    print("Redirecting to payments:select_method with booking_id=", booking.pk)
                    context = {
                        'flight': flight,
                        'adults': adults,
                        'children': children,
                        'infants': infants,
                        'total_passengers': total_passengers,
                        'total_price': total_price,
                    }
                    # return redirect('payments:select_method', booking_id=booking.pk)
                    return render(request, 'bookings/create_booking.html', context)
                    # return redirect('bookings:create_booking', pk=flight.pk)
                
                # ایجاد مسافران و اتصال به رزرو
                for i in range(total_passengers):
                    passenger = Passenger.objects.create(
                        user=request.user,
                        first_name=first_names[i],
                        last_name=last_names[i],
                        national_id=national_ids[i],
                        date_of_birth=birth_dates[i]
                    )
                    
                    # اختصاص صندلی ساده (A1, A2, B1, ...)
                    row = chr(65 + (i // 6))  # A, B, C, ...
                    col = (i % 6) + 1
                    seat_number = f"{row}{col}"
                    
                    BookingPassenger.objects.create(
                        booking=booking,
                        passenger=passenger,
                        seat_number=seat_number
                    )
                
                # کاهش صندلی موجود
                flight.available_seats -= total_passengers
                flight.save()
                
                messages.success(request, 'رزرو با موفقیت ثبت شد! حالا روش پرداخت را انتخاب کنید.')
                return redirect('payments:select_method', booking_id=booking.pk)
                
        except Exception as e:
            messages.error(request, 'خطایی در فرآیند رزرو رخ داد. لطفاً دوباره تلاش کنید.')
            print("خطای رزرو:", e)  # برای دیباگ
            
            # context رو دوباره تعریف کن یا به صفحه اصلی برگردون
            context = {
                'flight': flight,
                'adults': adults,
                'children': children,
                'infants': infants,
                'total_passengers': total_passengers,
                'total_price': total_price,
            }
            return render(request, 'bookings/create_booking.html', context)
    
    # GET - نمایش فرم رزرو
    context = {
        'flight': flight,
        'adults': adults,
        'children': children,
        'infants': infants,
        'total_passengers': total_passengers,
        'total_price': total_price,
    }
    return render(request, 'bookings/create_booking.html', context)

