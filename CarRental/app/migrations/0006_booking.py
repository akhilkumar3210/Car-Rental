# Generated by Django 5.1.6 on 2025-02-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_cars_rental'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.TimeField()),
                ('dropoff_location', models.CharField(max_length=255)),
                ('dropoff_date', models.DateField()),
                ('dropoff_time', models.TimeField()),
                ('status', models.CharField(default='Pending', max_length=100)),
            ],
        ),
    ]
