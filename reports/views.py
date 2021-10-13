from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.list import ListView
from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField
from pilot_log.models import FlightDetail

# Create your views here.
class ListReportsView(LoginRequiredMixin, ListView):

    model = FlightDetail

    def get_template_names(self):
        if self.request.user.is_supervisor:
            return ["reports.html"]        
        else:
            return ["unauthorized.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_supervisor:
            context['error'] = 'You must be a supervisor to view this page.'
        return context


class SupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_supervisor

    def handle_no_permission(self):
        messages.error(self.request, 'Only supervisors may view this page.')
        return redirect(reverse('unauthorized'))

class TotalTimesReportView(SupervisorRequiredMixin, SlickReportView):
    report_model = FlightDetail        
    date_field = 'date_of_flight'
    columns = ['pilot__last_name', 
                SlickReportField.create(
                    method=Sum,
                    field='total_time',
                    name='total_time__sum',
                    verbose_name=('Sum of Total Time'))
                ]
    group_by = 'pilot__last_name'

    chart_settings = [
            {
                'type': 'column',
                'data_source': ['total_time__sum'],
                'title_source': ['total_time'],
                'title': 'Total Time by Pilot',
                'title_source': 'pilot__last_name',
            }
        ]   
        
class NumMsnsFlownReportView(SupervisorRequiredMixin, SlickReportView):
    report_model = FlightDetail
    date_field = 'date_of_flight'
    group_by = 'msn_type'
    columns = [ 'msn_type' ]
    crosstab_model = 'pilot'
    crosstab_columns = [
        SlickReportField.create(
            method=Count,
            field='msn_type',
            name='msn_type__count',
            verbose_name=('Mission')
            )]