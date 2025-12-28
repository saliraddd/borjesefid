from django.urls import path
from .views import UserBookingListView, BookingDetailView, create_booking

app_name = 'bookings'

urlpatterns = [
    path('', UserBookingListView.as_view(), name='booking_list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('create/<int:pk>/', create_booking, name='create_booking'),]
