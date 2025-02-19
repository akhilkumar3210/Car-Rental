from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Makes(models.Model):
    makes=models.TextField()

class Cars(models.Model):
    cid=models.TextField()
    make = models.ForeignKey(Makes,on_delete=models.CASCADE)
    model = models.TextField()
    year = models.IntegerField()
    color = models.TextField()
    license_plate = models.CharField(max_length=20, unique=True)
    mileage = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
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



