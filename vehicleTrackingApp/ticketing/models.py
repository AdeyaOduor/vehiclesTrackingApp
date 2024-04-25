from django.contrib.auth.models import User
from django.db import models
from vehicles.models import Vehicle

class Ticketing(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='ticketing', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='ticketing')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

class TicketingForm(models.Model):
    ticketing = models.ForeignKey(Ticketing, related_name='tickets', on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    departure_date = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    mileage_km = models.CharField(max_length=255)
    return_date = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_tickets', on_delete=models.CASCADE)