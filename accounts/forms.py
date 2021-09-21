from django import forms
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm,
    )
from django.forms import widgets
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'region', 'user_supervisor', 'is_supervisor')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'region', 'user_supervisor', 'base',
            'office_phone', 'cell_phone', 'date_of_hire',
            'pilot_cert_number', 'atp', 'cfi', 'cfii', 'mei',
            'commercial_rating', 'medical_class', 'date_of_medical',
            'is_captain', 'smokejumper_msn_eval_date', 'equipment_eval_date',
            ]
        widgets = {
            'date_of_hire': widgets.DateInput(attrs={'type': 'date'}),
            'date_of_medical': widgets.DateInput(attrs={'type': 'date'}),
            'smokejumper_msn_eval_date': widgets.DateInput(attrs={'type': 'date'}),
            'equipment_eval_date': widgets.DateInput(attrs={'type': 'date'}),
            'medical_class': widgets.Select(choices=[
                ('1','1'),
                ('2','2'),
                ('3','3'),
            ])
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
