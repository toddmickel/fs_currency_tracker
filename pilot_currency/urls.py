from django.urls import path
from .views import CurrencyDetailView, CurrencyBoardView

urlpatterns = [
    path('', CurrencyDetailView.as_view(), name='currency_detail'),
    path('board/', CurrencyBoardView.as_view(), name='currency_board')
]