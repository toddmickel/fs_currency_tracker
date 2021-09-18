from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView, 
    UpdateView,
    DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FlightDetail
from django.urls import reverse_lazy

class FlightCreateView(LoginRequiredMixin, CreateView):
    model = FlightDetail
    template_name = "flight_new.html"
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
        form.instance.pilot = self.request.user
        form.instance.total_time = form.instance.pic_time +  form.instance.sic_time + form.instance.instructor_time
        return super().form_valid(form)

class FlightDetailView(LoginRequiredMixin, DetailView):
    model = FlightDetail
    template_name = "flight_detail.html"

class FlightListView(LoginRequiredMixin, ListView):
    model = FlightDetail
    template_name = "flight_detail.html"

class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = FlightDetail
    template_name = "flight_new_edit.html"
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

class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = FlightDetail
    template_name = "flight_new_delete.html"
    success_url = reverse_lazy('flight_list')

    


    

