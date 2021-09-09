from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from dateutil.relativedelta import relativedelta
from pilot_log.models import FlightDetail


def total_hours(user):
    return user.objects.annotate(total_hours=Sum('flightdetail__total_time'))

class CurrencyDetailView(LoginRequiredMixin, ListView):
    template_name = 'currency_detail.html'
    model = FlightDetail
    today = date.today()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(pilot=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        twelve_mo = self.object_list.filter(date_of_flight__range=(self.today + relativedelta(months=-12), self.today))
        six_mo = self.object_list.filter(date_of_flight__range=(self.today + relativedelta(months=-6), self.today))
        ninety_day = self.object_list.filter(date_of_flight__range=(self.today + relativedelta(days=-90), self.today))
        sixty_day = self.object_list.filter(date_of_flight__range=(self.today + relativedelta(days=-60), self.today))
        
        tt = self.object_list.aggregate(Sum('total_time'))
        context['total_time'] = float(f"{tt['total_time__sum']:.1f}")

        yr_total = twelve_mo.aggregate(Sum('total_time'))
        context['12_mo'] = float(f"{yr_total['total_time__sum']:.1f}")

        yr_heavy = twelve_mo.filter(tail_number__aircraft_type__contains='SD-3').aggregate(Sum('total_time'))
        context['12_mo_heavy'] = float(f"{yr_heavy['total_time__sum']:.1f}")

        inst_appch = six_mo.aggregate(Sum('instrument_appchs'))
        context['6_mo_inst'] = int(f"{inst_appch['instrument_appchs__sum']}")

        holds = six_mo.aggregate(Sum('holds'))
        context['6_mo_holds'] = int(f"{holds['holds__sum']}")

        landings = ninety_day.aggregate(Sum('day_landings'), Sum('night_landings'))
        context['90_day_landings'] = int(f"{landings['day_landings__sum']}") + int(f"{landings['night_landings__sum']}")
        context['90_day_nt_landings'] = int(f"{landings['night_landings__sum']}")
        context['latest_ldg'] = self.object_list.filter(Q(day_landings__gt=0) | Q(night_landings__gt=0)).latest().date_of_flight
        context['latest_nt_ldg'] = self.object_list.filter(night_landings__gt=0).latest().date_of_flight

        hours_ninety = ninety_day.aggregate(Sum('total_time'))
        context['90_day_time'] = float(f"{hours_ninety['total_time__sum']:.1f}")

        hours_sixty = sixty_day.aggregate(Sum('total_time'))
        context['60_day_time'] = float(f"{hours_sixty['total_time__sum']:.1f}")
        return context   