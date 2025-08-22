# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import render, get_object_or_404, redirect

# from .forms import NewVehiclesForm, EditVehiclesForm
# from .models import Category, Vehicle

# def vehicle_list(request):
#     query = request.GET.get('query', '')
#     category_id = request.GET.get('category', 0)
#     categories = Category.objects.all()
#     vehicles = Vehicle.objects.filter(is_ticketed=False)
#     if category_id:
#         vehicles = vehicles.filter(category_id=category_id)
#     if query:
#         vehicles = vehicles.filter(Q(make__icontains=query) | Q(description__icontains=query))
#     return render(request, 'vehicles/vehicles.html', {
#         'vehicles': vehicles,
#         'query': query,
#         'categories': categories,
#         'category_id': int(category_id),
#     })

# def detail(request, pk):
#     vehicle = get_object_or_404(Vehicle, pk=pk)
#     related_vehicles = Vehicle.objects.filter(category=vehicle.category, is_ticketed=False).exclude(pk=pk)[:2]
#     return render(request, 'vehicles/detail.html', {
#         'vehicle': vehicle,
#         'related_vehicles': related_vehicles,
#     })

# @login_required
# def new(request):
#     if request.method == 'POST':
#         form = NewVehiclesForm(request.POST, request.FILES)
#         if form.is_valid():
#             vehicle = form.save(commit=False)
#             vehicle.created_by = request.user
#             vehicle.save()
#             return redirect('vehicles:detail', pk=vehicle.id)
#     else:
#         form = NewVehiclesForm()
#         return render(request, 'vehicles/form.html', {
#             'form': form,
#             'title': 'New Vehicle',
#         })

# @login_required
# def edit(request, pk):
#     vehicle = get_object_or_404(Vehicle, pk=pk, created_by=request.user)
#     if request.method == 'POST':
#         form = EditVehiclesForm(request.POST, request.FILES, instance=vehicle)
#         if form.is_valid():
#             form.save()
#             return redirect('vehicles:detail', pk=vehicle.id)
#     else:
#         form = EditVehiclesForm(instance=vehicle)
#         return render(request, 'vehicles/form.html', {
#             'form': form,
#             'title': 'Edit Vehicle',
#         })

# @login_required
# def delete(request, pk):
#     vehicle = get_object_or_404(Vehicle, pk=pk, created_by=request.user)
#     vehicle.delete()
#     return redirect('dashboard:index')


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
