from django.db import models
from accounts.models import User
from django.conf import settings


class FlightDetail(models.Model):
    pilot = models.ForeignKey(
        'User', 
        on_delete=CASCADE, 
        blank=False, 
        null=False
        )
    date_of_flight = models.DateField(null=False, blank=False)
    tail_number = models.ForeignKey(
        'Aircraft', 
        on_delete=models.PROTECT, 
        blank=False, 
        null=False,
        )
    depart_ICAO = models.CharField(max_length=4, null=False, blank=False)
    arrival_ICAO = models.CharField(max_length=4, null=False, blank=False)
    msn_type = models.CharField(
        choices=settings.MISSION_CHOICES,
        null=False, 
        blank=False,
        )
    pic_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    sic_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    instructor_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    total_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    act_instrument_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    sim_instrument_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    instrument_appchs = models.IntegerField(null=True, blank=True)
    holds = models.IntegerField(null=True, blank=True)
    day_landings = models.IntegerField(null=False, blank=False)
    night_time = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    night_landings = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(max_length=250, blank=True, default='')

    def __str__(self):
        return '%s %s' % (self.pilot, self.date_of_flight)

class Aircraft(models.Model):
    TAIL_NUMBERS = [
        ('N162Z', 'N162Z'),
        ('N163Z', 'N163Z'),
        ('N174Z', 'N174Z'),
        ('N176Z', 'N176Z'),
    ]

    tail_number = models.CharField(
        choices=TAIL_NUMBERS,
        primary_key=True
        )
    aircraft_type = models.CharField(
        choices=settings.AIRCRAFT_TYPES,
        null=False, 
        blank=False
    )

    def __str__(self):
        return self.tail_number