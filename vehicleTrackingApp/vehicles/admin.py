from django.contrib import admin
from .models import *
# from .models import Category, Vehicle

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'county', 'subcounty']
    list_filter = ['user_type', 'county', 'subcounty']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'make', 'model', 'county', 'subcounty', 'status']
    list_filter = ['vehicle_type', 'status', 'county', 'subcounty']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'latitude', 'longitude', 'timestamp']
    list_filter = ['vehicle__county', 'vehicle__subcounty']

admin.site.register(WorkTicket)
admin.site.register(MaintenanceSchedule)
admin.site.register(Fueling)
admin.site.register(Category)
admin.site.register(Vehicle)


