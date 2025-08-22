# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('national', 'National Admin'),
        ('county', 'County Admin'),
        ('subcounty', 'Subcounty Admin'),
        ('driver', 'Driver'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    county = models.CharField(max_length=100, blank=True, null=True)
    subcounty = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('motorcycle', 'Motorcycle'),
        ('bus', 'Bus'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    color = models.CharField(max_length=30)
    vin = models.CharField(max_length=50, unique=True)
    county = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    current_driver = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='assigned_vehicle')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    mileage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make} {self.model}"

class Location(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.timestamp}"

class WorkTicket(models.Model):
    TICKET_TYPES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='work_tickets')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_tickets')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.get_ticket_type_display()}"

class MaintenanceSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mileage_at_service = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.maintenance_type}"

class Fueling(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuelings')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fuel_entries')
    date = models.DateTimeField(auto_now_add=True)
    liters = models.DecimalField(max_digits=6, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    station_name = models.CharField(max_length=100)
    station_location = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.liters}L"

# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('national', 'National Admin'),
        ('county', 'County Admin'),
        ('subcounty', 'Subcounty Admin'),
        ('driver', 'Driver'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    county = models.CharField(max_length=100, blank=True, null=True)
    subcounty = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('motorcycle', 'Motorcycle'),
        ('bus', 'Bus'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    color = models.CharField(max_length=30)
    vin = models.CharField(max_length=50, unique=True)
    county = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    current_driver = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='assigned_vehicle')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    mileage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make} {self.model}"

class Location(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.timestamp}"

class WorkTicket(models.Model):
    TICKET_TYPES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='work_tickets')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_tickets')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.get_ticket_type_display()}"

class MaintenanceSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mileage_at_service = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.maintenance_type}"

class Fueling(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuelings')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fuel_entries')
    date = models.DateTimeField(auto_now_add=True)
    liters = models.DecimalField(max_digits=6, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    station_name = models.CharField(max_length=100)
    station_location = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.liters}L"
