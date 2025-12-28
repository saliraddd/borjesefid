import requests
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from .models import Payment

ZARINPAL_URL = 'https://api.zarinpal.com/pg/v4/payment/'

def send_request(payment):
    callback_url = settings.ZARINPAL['callback_url']
    
    data = {
        "merchant_id": settings.ZARINPAL['merchant_id'],
        "amount": int(payment.amount),
        "description": f"پرداخت رزرو پرواز {payment.booking.booking_code}",
        "callback_url": callback_url,
    }
    
    response = requests.post(ZARINPAL_URL + 'request.json', json=data)
    result = response.json()
    
    if result['data']['code'] == 100:
        payment.authority = result['data']['authority']
        payment.save()
        url = f"https://{'www.' if not settings.ZARINPAL['sandbox'] else 'sandbox.'}zarinpal.com/pg/StartPay/{result['data']['authority']}"
        return redirect(url)
    else:
        return None


def verify_payment(authority, status):
    try:
        payment = Payment.objects.get(authority=authority)
    except Payment.DoesNotExist:
        return False, "پرداخت یافت نشد"
    
    if status != 'OK':
        payment.status = 'failed'
        payment.save()
        return False, "پرداخت لغو شد"
    
    data = {
        "merchant_id": settings.ZARINPAL['merchant_id'],
        "authority": authority,
        "amount": int(payment.amount),
    }
    
    response = requests.post(ZARINPAL_URL + 'verify.json', json=data)
    result = response.json()
    
    if result['data']['code'] in [100, 101]:
        payment.status = 'success'
        payment.ref_id = result['data']['ref_id']
        payment.save()
        
        # تغییر وضعیت رزرو
        payment.booking.status = 'confirmed'
        payment.booking.save()
        
        return True, result['data']['ref_id']
    else:
        payment.status = 'failed'
        payment.save()
        return False, result['data']['code']
    
