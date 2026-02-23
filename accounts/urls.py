from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .dashboard_views import (
    dashboard, dashboard_transactions, dashboard_bookings,
    dashboard_profile, charge_credit, withdrawal_request
)

app_name = 'accounts'

urlpatterns = [
    # احراز هویت
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('signup/customer/', views.customer_signup, name='signup_customer'),
    path('signup/agency/', views.agency_signup, name='signup_agency'),
    path('logout/', views.logout_view, name='logout'),

    # داشبورد (اگر هنوز داری)
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/transactions/', dashboard_transactions, name='transactions'),
    # ... بقیه مسیرهای داشبورد
]
