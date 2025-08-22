# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Vehicle, WorkTicket, MaintenanceSchedule, Fueling

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'county', 'subcounty', 'phone_number')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude = ['current_driver']

class WorkTicketForm(forms.ModelForm):
    class Meta:
        model = WorkTicket
        fields = ['ticket_type', 'description', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MaintenanceScheduleForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSchedule
        fields = ['maintenance_type', 'description', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FuelingForm(forms.ModelForm):
    class Meta:
        model = Fueling
        fields = ['liters', 'cost', 'mileage', 'station_name', 'station_location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from django.http import JsonResponse
from .models import *
from .forms import *
import json
from datetime import datetime, timedelta

def is_admin(user):
    return user.user_type in ['national', 'county', 'subcounty']

def admin_required(view_func):
    return login_required(user_passes_test(is_admin)(view_func))

@login_required
def dashboard(request):
    user = request.user
    
    # Get vehicles based on user jurisdiction
    if user.user_type == 'national':
        vehicles = Vehicle.objects.all()
    elif user.user_type == 'county':
        vehicles = Vehicle.objects.filter(county=user.county)
    elif user.user_type == 'subcounty':
        vehicles = Vehicle.objects.filter(county=user.county, subcounty=user.subcounty)
    else:
        vehicles = Vehicle.objects.filter(current_driver=user)
    
    # Statistics
    total_vehicles = vehicles.count()
    active_vehicles = vehicles.filter(status='active').count()
    maintenance_vehicles = vehicles.filter(status='maintenance').count()
    
    # Recent activities
    recent_locations = Location.objects.filter(vehicle__in=vehicles).order_by('-timestamp')[:10]
    recent_tickets = WorkTicket.objects.filter(vehicle__in=vehicles).order_by('-created_at')[:5]
    
    # Fuel consumption data for charts
    fuel_data = Fueling.objects.filter(vehicle__in=vehicles).values('vehicle__license_plate').annotate(
        total_liters=Sum('liters'),
        total_cost=Sum('cost')
    )
    
    context = {
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'recent_locations': recent_locations,
        'recent_tickets': recent_tickets,
        'fuel_data': list(fuel_data),
        'vehicles': vehicles,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def add_vehicle(request):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to add vehicles.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f"Vehicle {vehicle.license_plate} added successfully.")
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'add_vehicle.html', {'form': form})

@login_required
def assign_driver(request, vehicle_id):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to assign drivers.")
        return redirect('dashboard')
    
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(CustomUser, id=driver_id, user_type='driver')
        
        vehicle.current_driver = driver
        vehicle.save()
        messages.success(request, f"Driver {driver.username} assigned to vehicle {vehicle.license_plate}.")
        return redirect('vehicle_list')
    
    # Get available drivers in the same jurisdiction
    if request.user.user_type == 'national':
        drivers = CustomUser.objects.filter(user_type='driver')
    elif request.user.user_type == 'county':
        drivers = CustomUser.objects.filter(user_type='driver', county=request.user.county)
    else:
        drivers = CustomUser.objects.filter(user_type='driver', county=request.user.county, subcounty=request.user.subcounty)
    
    return render(request, 'assign_driver.html', {'vehicle': vehicle, 'drivers': drivers})

@login_required
def submit_work_ticket(request):
    if request.user.user_type != 'driver':
        messages.error(request, "Only drivers can submit work tickets.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = WorkTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.driver = request.user
            ticket.vehicle = request.user.assigned_vehicle
            ticket.save()
            messages.success(request, "Work ticket submitted successfully.")
            return redirect('driver_dashboard')
    else:
        form = WorkTicketForm()
    
    return render(request, 'submit_ticket.html', {'form': form})

@login_required
def submit_fueling(request):
    if request.user.user_type != 'driver':
        messages.error(request, "Only drivers can submit fueling records.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = FuelingForm(request.POST)
        if form.is_valid():
            fueling = form.save(commit=False)
            fueling.driver = request.user
            fueling.vehicle = request.user.assigned_vehicle
            fueling.save()
            messages.success(request, "Fueling record submitted successfully.")
            return redirect('driver_dashboard')
    else:
        form = FuelingForm()
    
    return render(request, 'submit_fueling.html', {'form': form})

@login_required
def update_location(request):
    if request.method == 'POST' and request.user.user_type == 'driver':
        try:
            data = json.loads(request.body)
            vehicle = request.user.assigned_vehicle
            
            Location.objects.create(
                vehicle=vehicle,
                latitude=data['latitude'],
                longitude=data['longitude'],
                speed=data.get('speed')
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error'})

@admin_required
def vehicle_locations(request):
    user = request.user
    
    if user.user_type == 'national':
        vehicles = Vehicle.objects.all()
    elif user.user_type == 'county':
        vehicles = Vehicle.objects.filter(county=user.county)
    else:
        vehicles = Vehicle.objects.filter(county=user.county, subcounty=user.subcounty)
    
    locations = []
    for vehicle in vehicles:
        latest_location = vehicle.locations.first()
        if latest_location:
            locations.append({
                'vehicle': vehicle.license_plate,
                'latitude': float(latest_location.latitude),
                'longitude': float(latest_location.longitude),
                'timestamp': latest_location.timestamp.isoformat(),
                'status': vehicle.status
            })
    
    return JsonResponse({'locations': locations})

@login_required
def driver_dashboard(request):
    if request.user.user_type != 'driver':
        return redirect('dashboard')
    
    vehicle = request.user.assigned_vehicle
    recent_tickets = WorkTicket.objects.filter(vehicle=vehicle).order_by('-created_at')[:5]
    recent_fuelings = Fueling.objects.filter(vehicle=vehicle).order_by('-date')[:5]
    
    context = {
        'vehicle': vehicle,
        'recent_tickets': recent_tickets,
        'recent_fuelings': recent_fuelings,
    }
    
    return render(request, 'driver_dashboard.html', context)


<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Tracking System</title>
    <!-- Material UI CSS -->
    <link href="https://unpkg.com/@material-ui/core@4.11.0/dist/material-ui.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!-- Leaflet CSS for maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</head>
<body>
    <nav class="mdc-top-app-bar">
        <div class="mdc-top-app-bar__row">
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
                <span class="mdc-top-app-bar__title">Vehicle Tracking System</span>
            </section>
            <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end">
                {% if user.is_authenticated %}
                <span class="mdc-top-app-bar__action-item">Welcome, {{ user.username }}</span>
                <a href="{% url 'logout' %}" class="mdc-button mdc-button--raised">Logout</a>
                {% endif %}
            </section>
        </div>
    </nav>

    <div class="mdc-drawer-app-content">
        <main class="main-content">
            <div class="mdc-top-app-bar--fixed-adjust">
                {% if messages %}
                {% for message in messages %}
                <div class="mdc-snackbar mdc-snackbar--leading">
                    <div class="mdc-snackbar__surface">
                        <div class="mdc-snackbar__label">{{ message }}</div>
                    </div>
                </div>
                {% endfor %}
                {% endif %}
                
                {% block content %}
                {% endblock %}
            </div>
        </main>
    </div>

    <!-- Material UI JS -->
    <script src="https://unpkg.com/@material-ui/core@4.11.0/dist/material-ui.min.js"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</body>
</html>


<!-- dashboard.html -->
{% extends 'base.html' %}

{% block content %}
<div class="mdc-layout-grid">
    <div class="mdc-layout-grid__inner">
        <!-- Statistics Cards -->
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>Total Vehicles</h3>
                    <h1>{{ total_vehicles }}</h1>
                </div>
            </div>
        </div>
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>Active Vehicles</h3>
                    <h1>{{ active_vehicles }}</h1>
                </div>
            </div>
        </div>
        <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3">
            <div class="mdc-card">
                <div class="mdc-card__content">
                    <h3>In Maintenance</h3>
                    <h1>{{ maintenance_vehicles }}</h1>
                </div>
            </div>
        </div>
    </div>

    <!-- Map Section -->
    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Vehicle Locations</h3>
                <div id="map" style="height: 400px;"></div>
            </div>
        </div>
    </div>

    <!-- Recent Activities -->
    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-6">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Recent Locations</h3>
                <ul class="mdc-list">
                    {% for location in recent_locations %}
                    <li class="mdc-list-item">
                        <span class="mdc-list-item__text">
                            {{ location.vehicle.license_plate }} - 
                            {{ location.latitude }}, {{ location.longitude }}
                            <span class="mdc-list-item__secondary-text">
                                {{ location.timestamp }}
                            </span>
                        </span>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>

    <div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-6">
        <div class="mdc-card">
            <div class="mdc-card__content">
                <h3>Recent Work Tickets</h3>
                <ul class="mdc-list">
                    {% for ticket in recent_tickets %}
                    <li class="mdc-list-item">
                        <span class="mdc-list-item__text">
                            {{ ticket.vehicle.license_plate }} - {{ ticket.get_ticket_type_display }}
                            <span class="mdc-list-item__secondary-text">
                                Status: {{ ticket.get_status_display }}
                            </span>
                        </span>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</div>

<script>
// Initialize map
var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Fetch and plot vehicle locations
fetch('{% url "vehicle_locations" %}')
    .then(response => response.json())
    .then(data => {
        data.locations.forEach(location => {
            L.marker([location.latitude, location.longitude])
                .addTo(map)
                .bindPopup(`
                    <b>${location.vehicle}</b><br>
                    Status: ${location.status}<br>
                    Last updated: ${new Date(location.timestamp).toLocaleString()}
                `);
        });
    });
</script>
{% endblock %}
