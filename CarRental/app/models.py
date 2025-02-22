from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Makes(models.Model):
    makes=models.TextField()

class Booking(models.Model):
    # Pickup details
    pickup_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    # Dropoff details
    dropoff_location = models.CharField(max_length=255)
    dropoff_date = models.DateField()
    dropoff_time = models.TimeField()

    # To store any additional info or status, if needed
    status = models.CharField(max_length=100, default='Pending')

class Cars(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    cid=models.TextField()
    make = models.ForeignKey(Makes,on_delete=models.CASCADE)
    model = models.TextField()
    year = models.IntegerField()
    bodytype=models.TextField()
    fuel=models.TextField(null=True,blank=True)
    transmission=models.TextField()
    mileage = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.FileField()


class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



