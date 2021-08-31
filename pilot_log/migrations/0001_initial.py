# Generated by Django 3.2.6 on 2021-08-31 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('tail_number', models.CharField(choices=[('N162Z', 'N162Z'), ('N163Z', 'N163Z'), ('N174Z', 'N174Z'), ('N176Z', 'N176Z')], max_length=10, primary_key=True, serialize=False)),
                ('aircraft_type', models.CharField(choices=[('SD-3', 'Sherpa'), ('KA', 'King Air'), ('206', 'C-206')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='FlightDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_flight', models.DateField()),
                ('depart_ICAO', models.CharField(max_length=4)),
                ('arrival_ICAO', models.CharField(max_length=4)),
                ('msn_type', models.CharField(choices=[('LP', 'Leadplane'), ('SJ', 'Smokejumper'), ('PP', 'Pilot Proficiency'), ('AD', 'Administrative'), ('OT', 'Civilian/Military'), ('AA', 'Air Attack'), ('MT', 'Maintenance'), ('LOG', 'Logistics'), ('ASM', 'Aerial Supervision Module'), ('HC', 'Helicopter'), ('IR', 'Infrared'), ('RC', 'Recon'), ('PH', 'Photo'), ('BC', 'Back Country')], max_length=20)),
                ('pic_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('sic_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('instructor_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('total_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('act_instrument_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('sim_instrument_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('instrument_appchs', models.IntegerField(blank=True, null=True)),
                ('holds', models.IntegerField(blank=True, null=True)),
                ('day_landings', models.IntegerField()),
                ('night_time', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('night_landings', models.IntegerField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', max_length=250)),
                ('pilot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tail_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pilot_log.aircraft')),
            ],
        ),
    ]
