from django.contrib.auth.decorators import login_required
from django.db.models import Q # make easier to search multiple fields
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewVehiclesForm, EditVehiclesForm
from .models import Categories, vehicles

def vehicles(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Categories.objects.all()
    vehicles = vehicles.objects.filter(is_ticketed=False)
    if category_id:
        vehicles = vehicles.filter(category_id=category_id)
    if query:
        vehicles = vehicles.filter(Q(make__icontains=query) | Q(description__icontains=query)) 
    return render(request, 'vehicles/vehicles.html',
    {'vehicles':vehicles,
     'query': query,
     'categories': categories,
     'category_id': int(category_id),
  })
    
def detail(request, pk):
    vehicles = get_object_or_404(vehicles, pk=pk)
    related_vehicles = vehicles.objects.filter(category=vehicles.category, is_ticketed=False).exclude(pk=pk)[0:2]
    return render(request, 'vehicles/detail.html',{'vehicles':vehicles
  'related_vehicles':related_vehicles,
  })
  
@login_required
def new(request):
    if request.method = 'POST':
       form = NewVehiclesForm(request.POST, request.Files)
       if form.is_valid():
           vehicles = form.save(commit=false)
           vehicle.created_by = request.user
           vehicles.save()
           return redirect('vehicles:detail', pk=vehicles.id)
     else:
           form = NewVehiclesForm()
           return render(request, 'vehicles/form.html', {
         'form': form
         'title': 'New Vehicle'
    }) 

@login_required
def edit(request, pk):
    vehicles = get_object_or_404(vehicles, pk=pk, created_by=request.user)
    if request.method = 'POST':
       form = EditVehiclesForm(request.POST, request.Files, instance=vehicles)
       if form.is_valid():
          
           form.save()
           return redirect('vehicles:detail', pk=vehicles.id)
     else:
           form = EditVehiclesForm(instance=vehicles)
           return render(request, 'vehicles/form.html', {
         'form': form
         'title': 'Edit Vehicle'
    }) 
    
@login_required
def delete(request, pk):
    vehicles = get_object_or_404(vehicles, pk=pk, created_by=request.user)
    vehicles.delete()
    return redirect('dashboard:index')