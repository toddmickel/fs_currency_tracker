from django import forms
from django.forms import widgets
from .models import FlightDetail

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
