from django.urls import path
from .views import CurrencyDetailView

urlpatterns = [
    path('', CurrencyDetailView.as_view(), name='currency_detail'),
]