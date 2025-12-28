from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from bookings.models import Booking
from .models import Payment
from .zarinpal import send_request, verify_payment  

@login_required
def select_payment_method(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='pending')
    context = {
        'booking': booking,
    }
    return render(request, 'payments/select_method.html', context)

# پرداخت از کیف پول
@login_required
@transaction.atomic
def pay_with_wallet(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='pending')
    
    if request.user.profile.wallet_balance < booking.total_price:
        messages.error(request, 'موجودی کیف پول کافی نیست')
        return redirect('payments:select_method', booking_id=booking.id)
    
    # کم کردن از کیف پول
    request.user.profile.wallet_balance -= booking.total_price
    request.user.profile.save()
    
    # ایجاد پرداخت موفق
    Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        status='success',
        payment_method='online_wallet'
    )
    
    # تأیید رزرو
    booking.status = 'confirmed'
    booking.save()
    
    messages.success(request, 'پرداخت از کیف پول با موفقیت انجام شد!')
    return redirect('bookings:booking_detail', pk=booking.id)

# خرید اعتباری (فعلاً placeholder – بعداً با سرویس واقعی وصل کن)
@login_required
def credit_purchase(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='pending')
    messages.info(request, 'خرید اعتباری به زودی فعال می‌شود!')
    return redirect('payments:select_method', booking_id=booking.id)

# پرداخت با زرین‌پال (همون قبلی)
@login_required
def initiate_zarinpal(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='pending')
    
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        status='pending',
        payment_method='bank_transfer'
    )
    
    result = send_request(payment)
    if result:
        return result
    messages.error(request, 'خطا در اتصال به زرین‌پال')
    return redirect('payments:select_method', booking_id=booking.id)

