from django.urls import path
from .views import (
    CurrencyDetailView, 
    CurrencyBoardView, 
    TotalTimesReportView,
    ListReportsView)

urlpatterns = [
    path('', CurrencyDetailView.as_view(), name='currency_detail'),
    path('<int:uid>/', CurrencyDetailView.as_view(), name='currency_detail'),
    path('board/', CurrencyBoardView.as_view(), name='currency_board'),
    path('12month/', TotalTimesReportView.as_view(), name='twelve_months'),
    path('reports/', ListReportsView.as_view(), name='reports'),
]