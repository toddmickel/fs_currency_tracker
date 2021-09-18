from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse


class CustomUser(AbstractUser):
    REGION_CHOICES = [
        ('1', '1 - Northern'),
        ('2', '2 - Rocky Mountain'),
        ('3', '3 - Southwestern'),
        ('4', '4 - Intermountain'),
        ('5', '5 - Pacific Southwest'),
        ('6', '6 - Pacific Northwest'),
        ('8', '8 - Southern'),
        ('9', '9 - Eastern'),
        ('10', '10 - Alaska'),
        ('WO', 'Washington Office'),
    ] 
    '''username = None
    email = models.EmailField(_('email address'), unique=True)'''
    region = models.CharField(
        max_length=4, 
        choices=REGION_CHOICES,
        default='WO',
        null=False, 
        blank=False
        )
    base = models.CharField(max_length=20, blank=True)
    office_phone = models.CharField(max_length=12, blank=True)
    cell_phone = models.CharField(max_length=12, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    pilot_cert_number = models.CharField(max_length=20, blank=True)
    atp = models.BooleanField(default=False)
    cfi = models.BooleanField(default=False)
    cfii = models.BooleanField(default=False)
    mei = models.BooleanField(default=False)
    commercial_rating = models.BooleanField(default=False)
    medical_class = models.IntegerField(null=True, blank=True) 
    date_of_medical = models.DateField(null=True, blank=True)
    user_supervisor = models.ForeignKey(
        'self', 
        on_delete=models.PROTECT, 
        limit_choices_to={'is_supervisor': True},
        blank=True, 
        null=True
        )
    is_supervisor = models.BooleanField(default=False)
    is_captain = models.BooleanField(default=False)
    smokejumper_msn_eval_date = models.DateField(null=True, blank=True)
    equipment_eval_date = models.DateField(null=True, blank=True)

    order = ('username',)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])
        
class MsnQual(models.Model):
    pilot = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    mission = models.CharField(
        max_length=20,
        choices=settings.MISSION_CHOICES,
        null=False,
        blank=False
    )
    mission_check_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return '%s %s' % (self.pilot.last_name, self.mission)

class AcftQual(models.Model):
    pilot = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    acft = models.CharField(
        max_length=15,
        choices=settings.AIRCRAFT_TYPES,
        null=False,
        blank=False
    )
    acft_check_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return '%s %s' % (self.pilot, self.acft)

