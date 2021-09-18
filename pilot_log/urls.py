from django.urls import path
from .views import (
    FlightCreateView, 
    FlightDetailView, 
    FlightListView,
    FlightCreateView,
    FlightUpdateView,
    FlightDeleteView,
)

urlpatterns = [
    path('new/', FlightCreateView.as_view(), name='flight_new'),
    path('<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('<int:pk>/edit/', FlightUpdateView.as_view(), name='flight_edit'),
    path('<int:pk>/delete/', FlightDeleteView.as_view(), name='flight_delete'),
    path('view/', FlightListView.as_view(), name='flight_list')
]