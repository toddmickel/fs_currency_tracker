import django.core.exceptions
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
        try:
            context['total_time'] = float(f"{tt['total_time__sum']:.1f}")
        except:
            context['total_time'] = 0.0

        yr_total = twelve_mo.aggregate(Sum('total_time'))
        try:
            context['12_mo'] = float(f"{yr_total['total_time__sum']:.1f}")
        except:
            context['12_mo'] = 0.0

        yr_heavy = twelve_mo.filter(tail_number__aircraft_type__contains='SD-3').aggregate(Sum('total_time'))
        try:
            context['12_mo_heavy'] = float(f"{yr_heavy['total_time__sum']:.1f}")
        except:
            context['12_mo_heavy'] = 0.0

        inst_appch = six_mo.aggregate(Sum('instrument_appchs'))
        try:
            context['6_mo_inst'] = int(f"{inst_appch['instrument_appchs__sum']}")
        except:
            context['6_mo_inst'] = 0

        try:
            context['latest_inst'] = self.object_list.filter(instrument_appchs__gt=0).latest().date_of_flight
        except:
            context['latest_inst'] = "None"

        holds = six_mo.aggregate(Sum('holds'))
        try:
            context['6_mo_holds'] = int(f"{holds['holds__sum']}")
        except:
            context['6_mo_holds'] = 0

        try:
            context['latest_hold'] = self.object_list.filter(holds__gt=0).latest().date_of_flight
        except:
            context['latest_hold'] = "None"

        try:
            sel_landings = ninety_day.filter(tail_number__aircraft_type__contains='206').aggregate(Sum('day_landings'), Sum('night_landings'))
            sel_ldg_tot = int(f"{sel_landings['day_landings__sum']}") + int(f"{sel_landings['night_landings__sum']}")
            context['sel_landings'] = sel_ldg_tot
        except:
            sel_ldg_tot = 0
            context['sel_landings'] = 0
            

        try:
            last_sel_ldg = self.object_list.filter(
                tail_number__aircraft_type__contains='206'
                ).filter(
                    Q(day_landings__gt=0) |
                    Q(night_landings__gt=0)
                ).latest().date_of_flight
            context['last_sel_ldg'] = last_sel_ldg        
        except:
            last_sel_ldg = date(2900, 1, 1)
            context['last_sel_ldg'] = "None"
        
        try:
            mel_landings = ninety_day.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')).aggregate(Sum('day_landings'), Sum('night_landings')
                )
            mel_ldg_tot = int(f"{mel_landings['day_landings__sum']}") + int(f"{mel_landings['night_landings__sum']}")
            context['mel_landings'] = mel_ldg_tot
        except:
            mel_ldg_tot = 0
            context['mel_landings'] = 0

        try:
            last_mel_ldg = self.object_list.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')   
                ).filter(
                    Q(day_landings__gt=0) |
                    Q(night_landings__gt=0)
                ).latest().date_of_flight
            context['last_mel_ldg'] = last_mel_ldg        
        except:
            last_mel_ldg = date(2900, 1, 1)
            context['last_mel_ldg'] = "None"

        try:
            sherpa_landings = ninety_day.filter(tail_number__aircraft_type__contains='SD-3').aggregate(Sum('day_landings'), Sum('night_landings'))
            sherpa_ldg_tot = int(f"{sherpa_landings['day_landings__sum']}") + int(f"{sherpa_landings['night_landings__sum']}")
            context['sherpa_landings'] = sherpa_ldg_tot
        except:
            sherpa_ldg_tot = 0
            context['sherpa_landings'] = 0

        try:
            last_sherpa_ldg = self.object_list.filter(
                tail_number__aircraft_type__contains='SD-3'
                ).filter(
                    Q(day_landings__gt=0) |
                    Q(night_landings__gt=0)
                ).latest().date_of_flight
            context['last_sherpa_ldg'] = last_sherpa_ldg
        except:
            last_sherpa_ldg = date(2900, 1, 1)
            context['last_sherpa_ldg'] = "None"

        context['crit_ldgs'] = get_crit_ldgs(
            last_sel_ldg, sel_ldg_tot, 
            last_mel_ldg, mel_ldg_tot, 
            last_sherpa_ldg
            )

        try:
            mel_nt_ldg_tot = int(f"{mel_landings['night_landings__sum']}")
            context['mel_nt_landings'] = mel_nt_ldg_tot
        except:
            mel_nt_ldg_tot = 0
            context['mel_nt_landings'] = 0

        try:
            last_mel_nt_ldg = self.object_list.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')   
                ).filter(night_landings__gt=0).latest().date_of_flight
            context['last_mel_nt_ldg'] = last_mel_nt_ldg        
        except:
            last_mel_nt_ldg = date(2900, 1, 1)
            context['last_mel_nt_ldg'] = "None"

        try:
            sherpa_nt_ldg_tot = int(f"{sherpa_landings['night_landings__sum']}")
            context['sherpa_nt_landings'] = sherpa_nt_ldg_tot
        except:
            sherpa_nt_ldg_tot = 0
            context['sherpa_nt_landings'] = 0

        try:
            last_sherpa_ldg = self.object_list.filter(
                tail_number__aircraft_type__contains='SD-3'
                ).filter(night_landings__gt=0).latest().date_of_flight
            context['last_sherpa_nt_ldg'] = last_sherpa_ldg
        except:
            last_sherpa_nt_ldg = date(2900, 1, 1)
            context['last_sherpa_nt_ldg'] = 'None'

        context['crit_nt_ldgs'] = get_crit_ldgs(
            date(2900, 1, 1), 0, 
            last_mel_ldg, mel_ldg_tot, 
            last_sherpa_ldg
            )

        try:
            sel_ninety_time = ninety_day.filter(tail_number__aircraft_type__contains='206').aggregate(Sum('total_time'))
            sel_ninety_tt = float(f"{sel_ninety_time['total_time__sum']}")
            context['sel_90_tt'] = sel_ninety_tt
        except:
            sel_ninety_tt = 0
            context['sel_90_tt'] = 0

        try: 
            last_sel_flt = self.object_list.filter(
                tail_number__aircraft_type__contains='206'
                ).filter(total_time__gt=0).latest().date_of_flight
            context['last_sel_flt'] = last_sel_flt
        except:
            last_sel_flt = date(2900, 1, 1)
            context['last_sel_flt'] = 'None'

        try:
            mel_ninety_time = ninety_day.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')).aggregate(Sum('total_time')
                )
            mel_ninety_tt = float(f"{mel_ninety_time['total_time__sum']}")
            context['mel_90_tt'] = mel_ninety_tt
        except:
            mel_ninety_tt = 0
            context['mel_90_tt'] = 0
        
        try:
            last_mel_flt = self.object_list.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')   
                ).filter(total_time__gt=0).latest().date_of_flight
            context['last_mel_flt'] = last_mel_flt
        except:
            last_mel_flt = date(2900, 1, 1)
            context['last_mel_flt'] = 'None'

        try:
            sherpa_ninety_time = ninety_day.filter(tail_number__aircraft_type__contains='SD-3').aggregate(Sum('total_time'))
            sherpa_ninety_tt = float(f"{sherpa_ninety_time['total_time__sum']}")
            context['sherpa_90_tt'] = sherpa_ninety_tt
        except:
            sherpa_ninety_tt = 0
            context['sherpa_90_tt'] = 0

        try:
            last_sherpa_flt = self.object_list.filter(
                tail_number__aircraft_type__contains='SD-3'
                ).filter(total_time__gt=0).latest().date_of_flight
            context['last_sherpa_flt'] = last_sherpa_flt
        except:
            last_sherpa_flt = date(2900, 1, 1)
            context['last_sherpa_flt'] = 'None'

        context['crit_90_tt'] = get_crit_tt(
            last_sel_flt, sel_ninety_tt,
            last_mel_flt, mel_ninety_tt,
            last_sherpa_flt
        )

        hours_ninety = ninety_day.aggregate(Sum('total_time'))
        try:
            context['90_day_time'] = float(f"{hours_ninety['total_time__sum']:.1f}")
        except:
            context['90_day_time'] = 0.0

        hours_sixty = sixty_day.aggregate(Sum('total_time'))
        try:
            context['60_day_time'] = float(f"{hours_sixty['total_time__sum']:.1f}")
        except:
            context['60_day_time'] = 0.0
        return context   

class CurrencyBoardView(LoginRequiredMixin, ListView):
    template_name = 'currency_board.html'
    model = FlightDetail
    today = date.today()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(pilot__user_supervisor=self.request.user.id)


def get_crit_ldgs(
    last_sel, sel_ldg, 
    last_mel, mel_ldg, 
    last_sherpa
    ):
    if last_sel < last_mel and last_sel < last_sherpa and sel_ldg > 0:
        return 'sel'
    elif last_mel < last_sherpa and mel_ldg > 0:
        return 'mel'
    else:
        return 'sherpa'

def get_crit_tt(
    last_sel, sel_tt,
    last_mel, mel_tt,
    last_sherpa
    ):
    if last_sel < last_mel and last_sel < last_sherpa and sel_tt > 0:
        return 'sel'
    elif last_mel < last_sherpa and mel_ldg > 0:
        return 'mel'
    else:
        return 'sherpa'    