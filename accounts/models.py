from django.db import models
from django.contrib.auto.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    region = models.CharField(max_length=4, null=False, blank=False)
    base = models.CharField(max_length=20, blank=True)
    office_phone = models.CharField(max_length=12, blank=True)
    cell_phone = models.CharField(Max_length=12, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    pilot_cert_number = models.CharField(max_length=20, blank=True)
    atp =models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []