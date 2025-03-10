from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
# Create your models here.



class Makes(models.Model):
    makes=models.TextField()

class Location(models.Model):
    location=models.TextField()



class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    # Unique booking identifier
    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Pickup details
    pickup_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    # Dropoff details
    dropoff_location = models.CharField(max_length=255)
    dropoff_date = models.DateField()
    dropoff_time = models.TimeField()

    # Booking status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Track which user made the booking
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    # Auto timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} | {self.pickup_location} → {self.dropoff_location} on {self.pickup_date}"

class Cars(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    cid=models.TextField()
    make = models.ForeignKey(Makes,on_delete=models.CASCADE)
    model = models.TextField()
    year = models.IntegerField()
    bodytype=models.TextField()
    fuel=models.TextField()
    transmission=models.TextField()
    mileage = models.IntegerField()
    price_per_day = models.IntegerField()
    description = models.TextField()
    image = models.FileField()
    is_available = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    driving_license_front = models.ImageField(upload_to='driving_licenses/', blank=True, null=True)
    driving_license_back = models.ImageField(upload_to='driving_licenses/', blank=True, null=True)


class Buy(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    # car =models.ForeignKey(Cars,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    tot_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)

class Rented(models.Model):
    buy=models.ForeignKey(Buy,on_delete=models.CASCADE)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    # car =models.ForeignKey(Cars,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    tot_price=models.IntegerField()

    


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(_("Payment Status"), default=PaymentStatus.PENDING,max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_('Signature ID'),max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"



