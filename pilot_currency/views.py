from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from pilot_log.models import FlightDetail


def total_hours(user):
    return user.objects.annotate(total_hours=Sum('flightdetail__total_time'))

class CurrencyDetailView(LoginRequiredMixin, ListView):
    template_name = 'currency_detail.html'
    model = FlightDetail

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(pilot=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        tt = FlightDetail.objects.aggregate(Sum('total_time'))
        context['total_time'] = tt['total_time__sum']
        return context