from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ListReportsView,
    TotalTimesReportView,
    NumMsnsFlownReportView,
)

urlpatterns = [
    path('', ListReportsView.as_view(), name='reports'),
    path('12month/', TotalTimesReportView.as_view(), name='twelve_months'),
    path('num_msns', NumMsnsFlownReportView.as_view(), name='num_msns'),
    path('unauthorized/', TemplateView.as_view(template_name='unauthorized.html'), name='unauthorized')
]