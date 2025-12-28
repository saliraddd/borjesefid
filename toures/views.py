from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Tour


class TourHomeView(TemplateView):
    template_name = 'toures/tour_home.html'

class TourListView(ListView):
    model = Tour
    template_name = 'toures/tour_list.html'  # بعداً می‌سازیم
    context_object_name = 'object_list'
    paginate_by = 12

    def get_queryset(self):
        queryset = Tour.objects.all()
        destination = self.request.GET.get('destination')
        departure_date = self.request.GET.get('departure_date')
        return_date = self.request.GET.get('return_date')
        passengers = self.request.GET.get('passengers')

        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if departure_date:
            queryset = queryset.filter(departure_date__gte=departure_date)
        if return_date:
            queryset = queryset.filter(return_date__lte=return_date)

        return queryset.order_by('departure_date')

class TourDetailView(DetailView):
    model = Tour
    template_name = 'toures/tour_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'tour'