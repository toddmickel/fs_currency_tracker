from django.urls import path
from .views import FlightCreateView, FlightDetailView

urlpatterns = [
    path('new/', FlightCreateView.as_view(), name='flight_new'),
    path('<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
]