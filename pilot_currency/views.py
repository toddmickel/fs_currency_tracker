import django.core.exceptions
from django.db.models import Sum, Q, Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from dateutil.relativedelta import relativedelta
from pilot_log.models import FlightDetail
from accounts.models import CustomUser

def total_hours(user):
    return user.objects.annotate(total_hours=Sum('flightdetail__total_time'))

class CurrencyDetailView(LoginRequiredMixin, ListView):
    template_name = 'currency_detail.html'
    model = FlightDetail

    def get_queryset(self):
        qs = super().get_queryset()
        try: self.kwargs['uid']
        except KeyError:
            return qs.filter(pilot=self.request.user.id)
        else:
            return qs.filter(pilot=self.kwargs['uid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        twelve_mo = get_12_mo_records(self.object_list)
        six_mo = get_6_mo_records(self.object_list)
        ninety_day = get_90_day_records(self.object_list)
        sixty_day = get_60_day_records(self.object_list)
        
        tt = self.object_list.aggregate(Sum('total_time'))
        try:
            context['total_time'] = float(f"{tt['total_time__sum']:.1f}")
        except:
            context['total_time'] = 0.0

        yr_currency = get_12_mo_currency_items(twelve_mo)
        for key in yr_currency:
            context[key] = yr_currency[key]


        six_mo_currency = get_6_mo_currency_items(six_mo)
        for key in six_mo_currency:
            context[key] = six_mo_currency[key]

        ninety_day_ldg_currency = get_90_day_landing_currency(ninety_day)
        for key in ninety_day_ldg_currency:
            context[key] = ninety_day_ldg_currency[key]

        ninety_day_nt_currency = get_90_day_nt_currency(ninety_day)
        for key in ninety_day_nt_currency:
            context[key] = ninety_day_nt_currency[key]

        ninety_day_tt_currency = get_90_day_tt_currency(ninety_day)
        for key in ninety_day_tt_currency:
            context[key] = ninety_day_tt_currency[key]

        return context

class CurrencyBoardView(LoginRequiredMixin, ListView):
    template_name = 'currency_board.html'
    model = CustomUser

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_supervisor=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['active_users'] = self.object_list.filter(is_active=True)
        except:
            context['active_users'] = None

        try:
            context['inactive_users'] = self.object_list.filter(is_active=False)
        except:
            context['inactive_users'] = None
        return context

class CurrencyStatusView(LoginRequiredMixin, ListView):
    template_name = 'currency_status.html'
    model = FlightDetail

    def get_queryset(self):
        qs = super().get_queryset()
        try: self.kwargs['uid']
        except KeyError:
            return qs.values('pilot__last_name').filter(pilot__user_supervisor=self.request.user.id)
        else:
            return qs.values('pilot__last_name').filter(pilot__user_supervisor=self.kwargs['uid']) 

    def get_context_data(self, **kwargs):
        context = {}
        results = {}
        i = 1
        for pilot in self.object_list.values('pilot__id', 'pilot__last_name', 'pilot__first_name').distinct().order_by('pilot__last_name', 'pilot__first_name'):
            pilot_records = self.object_list.filter(pilot__id=pilot['pilot__id'])

            twelve_mo_records = get_12_mo_records(pilot_records)
            twelve_mo_times = get_12_mo_currency_items(twelve_mo_records)
            # context['12_mo_' + pilot['pilot__last_name'] + '_' + pilot['pilot__first_name']] = check_12_mo_currency(twelve_mo_times)

            six_mo_records = get_6_mo_records(pilot_records)
            six_mo_times = get_6_mo_currency_items(six_mo_records)
            # context['6_mo_' + pilot['pilot__last_name'] + '_' + pilot['pilot__first_name']] = check_6_mo_currency(six_mo_times)

            ninety_day_records = get_90_day_records(pilot_records)
            ninety_day_landing = get_90_day_landing_currency(ninety_day_records)
            ninety_day_night = get_90_day_nt_currency(ninety_day_records)
            ninety_day_times = get_90_day_tt_currency(ninety_day_records)
            """ context['90_day_sel_' + pilot['pilot__last_name'] + '_' + pilot['pilot__first_name']] = (
                check_90_day_sel(ninety_day_landing, ninety_day_times))
            context['90_day_mel_' + pilot['pilot__last_name'] + '_' + pilot['pilot__first_name']] = (
                check_90_day_mel(ninety_day_landing, ninety_day_night, ninety_day_times))
            context['90_day_sherpa_' + pilot['pilot__last_name'] + '_' + pilot['pilot__first_name']] = (
                check_90_day_sherpa(ninety_day_landing, ninety_day_night, ninety_day_times)) """
            curr_status = {
                'pilot': pilot['pilot__last_name'] + ', ' + pilot['pilot__first_name'],
                'pilot_id': pilot['pilot__id'],
                '12_mo': check_12_mo_currency(twelve_mo_times),
                '6_mo': check_6_mo_currency(six_mo_times),
                '90_day_sel': check_90_day_sel(ninety_day_landing, ninety_day_times),
                '90_day_mel': check_90_day_mel(ninety_day_landing, ninety_day_night, ninety_day_times),
                '90_day_sherpa': check_90_day_sherpa(ninety_day_landing, ninety_day_night, ninety_day_times),
                }
            results['curr' + str(i)] = curr_status
            i += 1
        context['numrecs'] = range(i-1)
        context['results'] = results
        return context



def get_12_mo_records(object_list):
    obj = object_list.filter(date_of_flight__range=(date.today() + relativedelta(months=-12), date.today()))
    return obj

def get_6_mo_records(object_list):
    obj = object_list.filter(date_of_flight__range=(date.today() + relativedelta(months=-6), date.today()))
    return obj

def get_90_day_records(object_list):
    obj = object_list.filter(date_of_flight__range=(date.today() + relativedelta(days=-90), date.today()))
    return obj

def get_60_day_records(object_list):
    obj = object_list.filter(date_of_flight__range=(date.today() + relativedelta(days=-60), date.today()))
    return obj

def get_12_mo_currency_items(twelve_mo):
    currency = {
        "12_mo": 0.0,
        "12_mo_heavy": 0.0,
    }

    if twelve_mo:
        yr_total = twelve_mo.aggregate(Sum('total_time'))
        currency["12_mo"] = float(f"{yr_total['total_time__sum']:.1f}")

    yr_heavy = twelve_mo.filter(tail_number__aircraft_type__contains='SD-3')
    if yr_heavy:
        yr_heavy = yr_heavy.aggregate(Sum('total_time'))
        currency['12_mo_heavy'] = float(f"{yr_heavy['total_time__sum']:.1f}")

    return currency

def check_12_mo_currency(flight_records):
    yellow_flt_time = 100
    green_flt_time = 120
    yellow_lg_me_flt_time = 25
    green_lg_me_flt_time = 30

    if flight_records["12_mo"] >= green_flt_time and flight_records["12_mo_heavy"] >= green_lg_me_flt_time:
        return 'green'
    elif flight_records["12_mo"] < yellow_flt_time and flight_records["12_mo_heavy"] < yellow_lg_me_flt_time:
        return 'red'
    else:
        return 'yellow'


def get_6_mo_currency_items(six_mo):
    currency = {
        "6_mo_inst": 0,
        "latest_inst": "None",
        "6_mo_holds": 0,
        "latest_hold": "None",
    }

    if six_mo.filter(instrument_appchs__gt=0):
        inst_appch = six_mo.aggregate(Sum('instrument_appchs'))
        currency["6_mo_inst"] = int(f"{inst_appch['instrument_appchs__sum']}")
        try:
            currency["latest_inst"] = six_mo.filter(instrument_appchs__gt=0).latest().date_of_flight
        except:
            currency["latest_inst"] = date(2900, 1, 1)

    if six_mo.filter(holds__gt=0):
        holds = six_mo.aggregate(Sum('holds'))
        currency["6_mo_holds"] = int(f"{holds['holds__sum']}")
        try:
            currency["latest_hold"] = six_mo.filter(holds__gt=0).latest().date_of_flight
        except:
            currency["latest_hold"] = date(2900, 1, 1)

    return currency

def check_6_mo_currency(flight_records):
    yellow_inst = 6
    green_inst = 10
    yellow_hold = 1
    green_hold = 2

    if flight_records["6_mo_inst"] >= green_inst and flight_records["6_mo_holds"] >= green_hold:
        return 'green'
    elif flight_records["6_mo_inst"] < yellow_inst and flight_records["6_mo_holds"] < yellow_hold:
        return 'red'
    else:
        return 'yellow'

def get_90_day_landing_currency(ninety_day):
    currency = {
        "sel_landings": 0,
        "last_sel_ldg": "None",
        "mel_landings": 0,
        "last_mel_ldg": "None",
        "sherpa_landings": 0,
        "last_sherpa_ldg": "None",
    } 

    sel_landings_q = ninety_day.filter(tail_number__aircraft_type__contains='206')
    if sel_landings_q:
        sel_landings = sel_landings_q.aggregate(Sum('day_landings'), Sum('night_landings'))
        sel_ldg_tot = int(f"{sel_landings['day_landings__sum']}") + int(f"{sel_landings['night_landings__sum']}")
        currency['sel_landings'] = sel_ldg_tot
        try:
            last_sel_ldg = sel_landings_q.filter(
                Q(day_landings__gt=0) |
                Q(night_landings__gt=0)
            ).latest().date_of_flight
            currency['last_sel_ldg'] = last_sel_ldg
        except:
            last_sel_ldg = date(2900, 1, 1)
    else:
        last_sel_ldg = date(2900, 1, 1)
        sel_ldg_tot = 0
    
    mel_landings_q = ninety_day.filter(
        Q(tail_number__aircraft_type__contains='SD-3') | 
        Q(tail_number__aircraft_type__contains='King Air'))
    if mel_landings_q:
        mel_landings = mel_landings_q.aggregate(Sum('day_landings'), Sum('night_landings'))
        mel_ldg_tot = int(f"{mel_landings['day_landings__sum']}") + int(f"{mel_landings['night_landings__sum']}")
        currency['mel_landings'] = mel_ldg_tot
        try:
            last_mel_ldg = mel_landings_q.filter(
                Q(day_landings__gt=0) |
                Q(night_landings__gt=0)
            ).latest().date_of_flight
            currency['last_mel_ldg'] = last_mel_ldg
        except:
            last_mel_ldg = date(2900, 1, 1)
    else:
        last_mel_ldg = date(2900, 1, 1)
        mel_ldg_tot = 0

    sherpa_landings_q = ninety_day.filter(tail_number__aircraft_type__contains='SD-3')
    if sherpa_landings_q:
        sherpa_landings = sherpa_landings_q.aggregate(Sum('day_landings'), Sum('night_landings'))
        sherpa_ldg_tot = int(f"{sherpa_landings['day_landings__sum']}") + int(f"{sherpa_landings['night_landings__sum']}")
        currency['sherpa_landings'] = sherpa_ldg_tot
        try:
            last_sherpa_ldg = sherpa_landings_q.filter(
                Q(day_landings__gt=0) |
                Q(night_landings__gt=0)
            ).latest().date_of_flight
            currency['last_sherpa_ldg'] = last_sherpa_ldg
        except:
            last_sherpa_ldg = date(2900, 1, 1)
    else:
        last_sherpa_ldg = date(2900, 1, 1)
        sherpa_ldg_tot = 0

    currency['crit_ldgs'] = get_crit_ldgs(
        last_sel_ldg, sel_ldg_tot, 
        last_mel_ldg, mel_ldg_tot, 
        last_sherpa_ldg
    )

    return currency

def get_90_day_nt_currency(ninety_day):
    currency = {
        "mel_nt_landings": 0,
        "last_mel_nt_ldg": "None",
        "sherpa_nt_landings": 0,
        "last_sherpa_nt_ldg": None,
    }

    mel_nt_landings_q = ninety_day.filter(
        Q(tail_number__aircraft_type__contains='SD-3') | 
        Q(tail_number__aircraft_type__contains='King Air')).filter(
            night_landings__gt=0
    )
    if mel_nt_landings_q:
        mel_nt_landings = mel_nt_landings_q.aggregate(Sum('night_landings'))
        mel_nt_ldg_tot = int(f"{mel_nt_landings['night_landings__sum']}")
        currency['mel_nt_landings'] = mel_nt_ldg_tot
        try:
            last_mel_nt_ldg = mel_nt_landings_q.latest().date_of_flight
        except:
            last_mel_nt_ldg = date(2900, 1, 1)
        currency['last_mel_nt_ldg'] = last_mel_nt_ldg
    else:
        mel_nt_ldg_tot = 0
        last_mel_nt_ldg = date(2900, 1, 1)

    sherpa_nt_landings_q = ninety_day.filter(
        tail_number__aircraft_type__contains='SD-3'
        ).filter(night_landings__gt=0
    )
    if sherpa_nt_landings_q:
        sherpa_nt_landings = sherpa_nt_landings_q.aggregate(Sum('night_landings'))
        sherpa_nt_ldg_tot = int(f"{sherpa_nt_landings['night_landings__sum']}")
        currency['sherpa_nt_landings'] = sherpa_nt_ldg_tot
        try:
            last_sherpa_nt_ldg = sherpa_nt_landings_q.latest().date_of_flight
        except:
            last_sherpa_nt_ldg = date(2900, 1, 1)
        currency['last_sherpa_nt_ldg'] = last_sherpa_nt_ldg
    else:
        sherpa_nt_ldg_tot = 0
        last_sherpa_nt_ldg = date(2900, 1, 1)
    
    currency['crit_nt_ldgs'] = get_crit_ldgs(
        date(2900, 1, 1), 0, 
        last_mel_nt_ldg,
        mel_nt_ldg_tot,
        last_sherpa_nt_ldg
        )

    return currency


def get_90_day_tt_currency(ninety_day):
    currency = {
        "sel_90_tt": 0.0,
        "last_sel_flt": "None",
        "mel_90_tt": 0.0,
        "last_mel_flt": "None",
        "sherpa_90_tt": 0.0,
        "last_sherpa_flt": "None",
        "90_day_time": 0.0,
    }

    sel_ninety_time_q = ninety_day.filter(tail_number__aircraft_type__contains='206')
    if sel_ninety_time_q:
        sel_ninety_time = sel_ninety_time_q.aggregate(Sum('total_time'))
        sel_ninety_tt = float(f"{sel_ninety_time['total_time__sum']}")
        currency['sel_90_tt'] = sel_ninety_tt
        try:
            last_sel_flt = sel_ninety_time_q.filter(total_time__gt=0).latest().date_of_flight
        except:
            last_sel_flt = date(2900, 1, 1)
        currency['last_sel_flt'] = last_sel_flt
    else:
        sel_ninety_tt = 0
        last_sel_flt = date(2900, 1, 1)

    mel_ninety_time_q = ninety_day.filter(
        Q(tail_number__aircraft_type__contains='SD-3') | 
        Q(tail_number__aircraft_type__contains='King Air')
    )
    if mel_ninety_time_q:
        mel_ninety_time = mel_ninety_time_q.aggregate(Sum('total_time'))
        mel_ninety_tt = float(f"{mel_ninety_time['total_time__sum']}")
        currency['mel_90_tt'] = mel_ninety_tt
        try:
            last_mel_flt = mel_ninety_time_q.filter(total_time__gt=0).latest().date_of_flight
        except:
            last_mel_flt = date(2900, 1, 1)
        currency['last_mel_flt'] = last_mel_flt
    else:
        mel_ninety_tt = 0
        last_mel_flt = date(2900, 1, 1)

    sherpa_ninety_time_q = ninety_day.filter(tail_number__aircraft_type__contains='SD-3')
    if sherpa_ninety_time_q:
        sherpa_ninety_time = sherpa_ninety_time_q.aggregate(Sum('total_time'))
        sherpa_ninety_tt = float(f"{sherpa_ninety_time['total_time__sum']}")
        currency['sherpa_90_tt'] = sherpa_ninety_tt
        try:
            last_sherpa_flt = sherpa_ninety_time_q.filter(total_time__gt=0).latest().date_of_flight
        except:
            last_sherpa_flt = date(2900, 1, 1)
        currency['last_sherpa_flt'] = last_sherpa_flt
    else:
        sherpa_ninety_tt = 0
        last_sherpa_flt = date(2900, 1, 1)

    currency['crit_90_tt'] = get_crit_tt(
        last_sel_flt, sel_ninety_tt,
        last_mel_flt, mel_ninety_tt,
        last_sherpa_flt
    )

    return currency

def check_90_day_sel(flight_records_ldg, flight_records_tt):
    yellow_ldg = 3
    green_ldg = 6
    yellow_tt = 1
    green_tt = 6

    if flight_records_ldg["sel_landings"] >= green_ldg and flight_records_tt["sel_90_tt"] >= green_tt:
        return 'green'
    elif flight_records_ldg["sel_landings"] < yellow_ldg and flight_records_tt["sel_90_tt"] < yellow_tt:
        return 'red'
    else:
        return 'yellow'

def check_90_day_mel(flight_records_ldg, flight_records_nt, flight_records_tt):
    yellow_ldg = 3
    green_ldg = 6
    green_nt_ldg = 3
    yellow_tt = 1
    green_tt = 6

    if (
        flight_records_ldg["mel_landings"] >= green_ldg and 
        flight_records_nt["mel_nt_landings"] >= green_nt_ldg and 
        flight_records_tt["mel_90_tt"] >= green_tt):
            return 'green'
    elif (
        flight_records_ldg["mel_landings"] < yellow_ldg and 
        flight_records_nt["mel_nt_landings"] < green_nt_ldg and
        flight_records_tt["mel_90_tt"] < yellow_tt):
            return 'red'
    else:
        return 'yellow'

def check_90_day_sherpa(flight_records_ldg, flight_records_nt, flight_records_tt):
    yellow_ldg = 3
    green_ldg = 6
    green_nt_ldg = 3
    yellow_tt = 1
    green_tt = 6

    if (
        flight_records_ldg["sherpa_landings"] >= green_ldg and 
        flight_records_nt["sherpa_nt_landings"] >= green_nt_ldg and 
        flight_records_tt["sherpa_90_tt"] >= green_tt):
            return 'green'
    elif (
        flight_records_ldg["sherpa_landings"] < yellow_ldg and 
        flight_records_nt["sherpa_nt_landings"] < green_nt_ldg and
        flight_records_tt["sherpa_90_tt"] < yellow_tt):
            return 'red'
    else:
        return 'yellow'

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