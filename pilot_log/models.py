from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from django.urls import reverse


class FlightDetail(models.Model):
    pilot = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete = models.CASCADE, 
        blank=False, 
        null=False,
        )
    date_of_flight = models.DateField(null=False, blank=False)
    tail_number = models.ForeignKey(
        'Aircraft', 
        on_delete = models.PROTECT, 
        blank=False, 
        null=False,
        )
    depart_ICAO = models.CharField(max_length=4, null=False, blank=False, default="KMSO")
    arrival_ICAO = models.CharField(max_length=4, null=False, blank=False, default="KMSO")
    msn_type = models.CharField(
        max_length=20,
        choices=settings.MISSION_CHOICES,
        null=False, 
        blank=False,
        )
    pic_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    sic_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    instructor_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    total_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    act_instrument_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    sim_instrument_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    instrument_appchs = models.IntegerField(default=0)
    holds = models.IntegerField(default=0)
    day_landings = models.IntegerField(default=0)
    night_time = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    night_landings = models.IntegerField(default=0)
    remarks = models.TextField(max_length=250, blank=True, default='')

    class Meta:
        ordering = ['-date_of_flight']
        get_latest_by = 'date_of_flight'

    def __str__(self):
        return '%s |  %s' % (self.pilot, self.date_of_flight)
    
    def get_absolute_url(self):
        return reverse('flight_detail', args=[str(self.id)])

class Aircraft(models.Model):

    tail_number = models.CharField(
        max_length=10,
        primary_key=True
        )
    aircraft_type = models.CharField(
        max_length=15,
        choices=settings.AIRCRAFT_TYPES,
        null=False, 
        blank=False
    )


    def __str__(self):
        return f'{self.tail_number} | {self.aircraft_type}'