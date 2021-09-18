from django import forms
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm,
    )
from functools import partial
from .models import CustomUser

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'region', 'user_supervisor', 'is_supervisor')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email',
            'region', 'user_supervisor', 'base',
            'office_phone', 'cell_phone', 'date_of_hire',
            'pilot_cert_number', 'atp', 'cfi', 'cfii', 'mei',
            'commercial_rating', 'medical_class', 'date_of_medical',
            'is_captain', 'smokejumper_msn_eval_date', 'equipment_eval_date',
            ]
