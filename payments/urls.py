from django.urls import path
from .views import initiate_zarinpal, verify_payment, select_payment_method, pay_with_wallet, credit_purchase

app_name = 'payments'

urlpatterns = [
    path('select/<int:booking_id>/', select_payment_method, name='select_method'),
    path('wallet/<int:booking_id>/', pay_with_wallet, name='pay_with_wallet'),
    path('credit/<int:booking_id>/', credit_purchase, name='credit_purchase'),
    path('zarinpal/<int:booking_id>/', initiate_zarinpal, name='initiate_zarinpal'),
    path('verify/', verify_payment, name='verify'),
]

