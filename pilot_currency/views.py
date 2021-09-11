from django.core.exceptions import ObjectDoesNotExist
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
        try:
            context['latest_inst'] = self.object_list.filter(instrument_appchs__gt=0).latest().date_of_flight
        except ObjectDoesNotExist:
            context['latest_inst'] = "None"

        holds = six_mo.aggregate(Sum('holds'))
        context['6_mo_holds'] = int(f"{holds['holds__sum']}")
        try:
            context['latest_hold'] = self.object_list.filter(holds__gt=0).latest().date_of_flight
        except ObjectDoesNotExist:
            context['latest_hold'] = "None"

        try:
            sel_landings = ninety_day.filter(tail_number__aircraft_type__contains='206').aggregate(Sum('day_landings'), Sum('night_landings'))
            sel_ldg_tot = int(f"{sel_landings['day_landings__sum']}") + int(f"{sel_landings['night_landings__sum']}")
            context['sel_landings'] = sel_ldg_tot
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
            last_sel_ldg = date(2900, 1, 1)
            context['last_sel_ldg'] = "None"
        
        try:
            mel_landings = ninety_day.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')).aggregate(Sum('day_landings'), Sum('night_landings')
                )
            mel_ldg_tot = int(f"{mel_landings['day_landings__sum']}") + int(f"{mel_landings['night_landings__sum']}")
            context['mel_landings'] = mel_ldg_tot
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
            last_mel_ldg = date(2900, 1, 1)
            context['last_mel_ldg'] = "None"

        try:
            sherpa_landings = ninety_day.filter(tail_number__aircraft_type__contains='SD-3').aggregate(Sum('day_landings'), Sum('night_landings'))
            sherpa_ldg_tot = int(f"{sherpa_landings['day_landings__sum']}") + int(f"{sherpa_landings['night_landings__sum']}")
            context['sherpa_landings'] = sherpa_ldg_tot
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
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
        except ObjectDoesNotExist:
            mel_nt_ldg_tot = 0
            context['mel_nt_landings'] = 0

        try:
            last_mel_nt_ldg = self.object_list.filter(
                Q(tail_number__aircraft_type__contains='SD-3') | 
                Q(tail_number__aircraft_type__contains='King Air')   
                ).filter(night_landings__gt=0).latest().date_of_flight
            context['last_mel_nt_ldg'] = last_mel_nt_ldg        
        except ObjectDoesNotExist:
            last_mel_nt_ldg = date(2900, 1, 1)
            context['last_mel_nt_ldg'] = "None"

        try:
            sherpa_nt_ldg_tot = int(f"{sherpa_landings['night_landings__sum']}")
            context['sherpa_nt_landings'] = sherpa_nt_ldg_tot
        except ObjectDoesNotExist:
            sherpa_nt_ldg_tot = 0
            context['sherpa_nt_landings'] = 0

        try:
            last_sherpa_ldg = self.object_list.filter(
                tail_number__aircraft_type__contains='SD-3'
                ).filter(night_landings__gt=0).latest().date_of_flight
            context['last_sherpa_nt_ldg'] = last_sherpa_ldg
        except ObjectDoesNotExist:
            last_sherpa_nt_ldg = date(2900, 1, 1)
            context['last_sherpa_nt_ldg'] = "None"

        context['crit_nt_ldgs'] = get_crit_ldgs(
            date(2900, 1, 1), 0, 
            last_mel_ldg, mel_ldg_tot, 
            last_sherpa_ldg
            )

        try:
            context['last_landing'] = self.object_list.filter(
                Q(day_langings__gt=0) |
                Q(night_landings__gt=0)
            ).latest().date_of_flight
        except:
            context['last_landing'] = "None"

        try:
            context['last_nt_ldg'] = self.object_list.filter(night_landings__gt=0).latest().date_of_flight
        except:
            context['last_nt_ldg'] = "None"

        hours_ninety = ninety_day.aggregate(Sum('total_time'))
        context['90_day_time'] = float(f"{hours_ninety['total_time__sum']:.1f}")

        hours_sixty = sixty_day.aggregate(Sum('total_time'))
        context['60_day_time'] = float(f"{hours_sixty['total_time__sum']:.1f}")
        return context   

def get_crit_ldgs(
    sel, sel_ldg, 
    mel, mel_ldg, 
    sherpa):
    if sel < mel and sel < sherpa and sel_ldg != 0:
        return 'sel'
    elif mel < sherpa and mel and mel_ldg !=0:
        return 'mel'
    else:
        return 'sherpa'