from django import forms
from django.forms import widgets
from .models import FlightDetail
import datetime

class NewFlightForm(forms.ModelForm):
    class Meta:
        model = FlightDetail
        exclude = ['pilot', 'total_time']
        widgets = {
            'date_of_flight': widgets.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yy',
                    'type': 'date',
                    }
                )
        }

    def __init__(self, *args, **kwargs):
        super(NewFlightForm, self).__init__(*args, **kwargs)

        self.fields['depart_ICAO'].widget.attrs['size'] = 4
        self.fields['arrival_ICAO'].widget.attrs['size'] = 4
        self.fields['pic_time'].widget.attrs['min'] = 0.0
        self.fields['sic_time'].widget.attrs['min'] = 0.0
        self.fields['instructor_time'].widget.attrs['min'] = 0.0
        self.fields['act_instrument_time'].widget.attrs['min'] = 0.0
        self.fields['sim_instrument_time'].widget.attrs['min'] = 0.0
        self.fields['night_time'].widget.attrs['min'] = 0.0

class FlightListFilterForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()