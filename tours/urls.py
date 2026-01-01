from django.urls import path
from .views import TourHomeView, TourListView, TourDetailView  

app_name = 'tours' 

urlpatterns = [
    path('', TourHomeView.as_view(), name='tour_home'),
    path('list/', TourListView.as_view(), name='tour_list'),
    path('<slug:slug>/', TourDetailView.as_view(), name='tour_detail'),
]