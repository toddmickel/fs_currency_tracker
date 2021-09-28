from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FlightDetail
from django.urls import reverse, reverse_lazy
from .forms import NewFlightForm, FlightListFilterForm
from datetime import date
import datetime
from django.http import HttpRequest
from django.core.exceptions import ImproperlyConfigured

class FlightCreateView(LoginRequiredMixin, CreateView):
    form_class = NewFlightForm
    template_name = "flight_new.html"

    def form_valid(self, form):
        form.instance.pilot = self.request.user
        form.instance.total_time = form.instance.pic_time +  form.instance.sic_time + form.instance.instructor_time
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('flight_list')

class FlightDetailView(LoginRequiredMixin, DetailView):
    model = FlightDetail
    template_name = "flight_detail.html"

class FlightListView(LoginRequiredMixin, ListView):
    model = FlightDetail
    form_class = FlightListFilterForm
    template_name = "view_flights.html"
    start_date = ''
    end_date = ''

    def get_start_date(self):
        start_date = self.start_date
        try:
            start_date = self.request.GET['start_date']
        except:
            start_date = ''
        if start_date is '':
            start_date = date.today() - datetime.timedelta(weeks=2600)
        return start_date

    def get_end_date(self):
        end_date = self.end_date
        try:
            end_date = self.request.GET['end_date']
        except:
            end_date = ''
        if end_date is '':
            end_date = date.today()
        return end_date    

    def get_queryset(self):
        qs = super().get_queryset()
        start = self.get_start_date()
        end = self.get_end_date()

        qs = qs.filter(
            date_of_flight__gte=start,
            date_of_flight__lte= end
            )
        return qs

class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = FlightDetail
    template_name = "flight_edit.html"
    fields = [
        "date_of_flight",
        "tail_number",
        "depart_ICAO",
        "arrival_ICAO",
        "msn_type",
        "pic_time",
        "sic_time",
        "instructor_time",
        "act_instrument_time",
        "sim_instrument_time",
        "instrument_appchs",
        "holds",
        "day_landings",
        "night_time",
        "night_landings",
        "remarks"
        ]

    def form_valid(self, form):
        form.instance.total_time = form.instance.pic_time +  form.instance.sic_time + form.instance.instructor_time
        return super().form_valid(form)

class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = FlightDetail
    template_name = "flight_delete.html"
    success_url = reverse_lazy('flight_list')

    


    

