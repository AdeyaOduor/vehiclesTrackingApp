from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewVehiclesForm, EditVehiclesForm
from .models import Category, Vehicle

def vehicle_list(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    vehicles = Vehicle.objects.filter(is_ticketed=False)
    if category_id:
        vehicles = vehicles.filter(category_id=category_id)
    if query:
        vehicles = vehicles.filter(Q(make__icontains=query) | Q(description__icontains=query))
    return render(request, 'vehicles/vehicles.html', {
        'vehicles': vehicles,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    related_vehicles = Vehicle.objects.filter(category=vehicle.category, is_ticketed=False).exclude(pk=pk)[:2]
    return render(request, 'vehicles/detail.html', {
        'vehicle': vehicle,
        'related_vehicles': related_vehicles,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewVehiclesForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.created_by = request.user
            vehicle.save()
            return redirect('vehicles:detail', pk=vehicle.id)
    else:
        form = NewVehiclesForm()
        return render(request, 'vehicles/form.html', {
            'form': form,
            'title': 'New Vehicle',
        })

@login_required
def edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditVehiclesForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicles:detail', pk=vehicle.id)
    else:
        form = EditVehiclesForm(instance=vehicle)
        return render(request, 'vehicles/form.html', {
            'form': form,
            'title': 'Edit Vehicle',
        })

@login_required
def delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, created_by=request.user)
    vehicle.delete()
    return redirect('dashboard:index')