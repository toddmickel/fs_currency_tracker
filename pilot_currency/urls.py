from django.urls import path
from .views import (
    CurrencyDetailView, 
    CurrencyBoardView,
    CurrencyStatusView, 
)

urlpatterns = [
    path('', CurrencyDetailView.as_view(), name='currency_detail'),
    path('<int:uid>/', CurrencyDetailView.as_view(), name='currency_detail'),
    path('board/', CurrencyBoardView.as_view(), name='currency_board'),
    path('status/', CurrencyStatusView.as_view(), name="currency_status"),
]