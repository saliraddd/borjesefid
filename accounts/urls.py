from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .dashboard_views import (
    dashboard, dashboard_transactions, dashboard_bookings,
    dashboard_profile, charge_credit, withdrawal_request
)

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/transactions/', dashboard_transactions, name='transactions'),
    path('dashboard/bookings/', dashboard_bookings, name='bookings'),
    path('dashboard/profile/', dashboard_profile, name='profile'),
    path('dashboard/charge/', charge_credit, name='charge'),
    path('dashboard/withdrawal/', withdrawal_request, name='withdrawal'),
]
