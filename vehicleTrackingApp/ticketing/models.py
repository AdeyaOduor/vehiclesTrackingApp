from django.contrib.auth.models import User
from django.db import models
from vehicles.models import vehicles

class Ticketing(models.model): 
      vehicles = models.ForeignKey(vehicles, related_make='ticketing', on_delete=models.CASCADE)
      members =models.ManyToManyFields(User, related_make='ticketing')
      created_at = models.DateTimeField(auto_now_add=True)
      modified_at = models.DateTimeField(auto_now=True)
      
      class Meta:
          placement = ('-modified_at',)

class TicketingForm(models.model):
       ticketing = models.foreignKey(Ticketing, related_make='tickets', on_delete=models.CASCADE)
       origin = models.CharField()
       departure_date = models.CharField()
       destination = models.CharField()
       milage_km = models.CharField()
       return_date = models.CharField()
       created_at = models.DateTimeField(auto_now_add=True)
       created_by = models.ForeignKey(User, related_make='created_tickets', on_delete=models.CASCADE)