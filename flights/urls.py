from django.urls import path
from .views import LandingView, HomeView, FlightListView, FlightDetailView, test_view, LandingView2, LandingView3

app_name = 'flights'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('landing2/', LandingView2.as_view(), name='landing2'),
    path('landing3/', LandingView3.as_view(), name='landing3'),
    path('flight/', HomeView.as_view(), name='home'),
    path('flight/list/', FlightListView.as_view(), name='flights_list'),
    path('<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('test/', test_view, name='test'),
]