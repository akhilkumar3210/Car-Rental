# Generated by Django 5.1.6 on 2025-03-10 07:56

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_remove_booking_user_remove_rented_booking_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Customer Name')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('status', models.CharField(default='Pending', max_length=254, verbose_name='Payment Status')),
                ('provider_order_id', models.CharField(max_length=40, verbose_name='Order ID')),
                ('payment_id', models.CharField(max_length=36, verbose_name='Payment ID')),
                ('signature_id', models.CharField(max_length=128, verbose_name='Signature ID')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('pickup_location', models.CharField(max_length=255)),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.TimeField()),
                ('dropoff_location', models.CharField(max_length=255)),
                ('dropoff_date', models.DateField()),
                ('dropoff_time', models.TimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.TextField()),
                ('model', models.TextField()),
                ('year', models.IntegerField()),
                ('bodytype', models.TextField()),
                ('fuel', models.TextField()),
                ('transmission', models.TextField()),
                ('mileage', models.IntegerField()),
                ('price_per_day', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('is_available', models.BooleanField(default=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.makes')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('date_of_birth', models.DateField()),
                ('driving_license_front', models.ImageField(blank=True, null=True, upload_to='driving_licenses/')),
                ('driving_license_back', models.ImageField(blank=True, null=True, upload_to='driving_licenses/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tot_price', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Rented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tot_price', models.IntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
                ('buy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.buy')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
