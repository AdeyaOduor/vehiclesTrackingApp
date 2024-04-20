from django.shortcuts import render, redirect
from vehicles.models import Category, vehicles
from .forms import SignupForm

def index(request):
    vehicles = vehicles.objects.filter(is_ticketed=False)[0:3]
    categories = Category.objects.all()
    return render(request, add_vehicles/'index.html', {'categories': categories, 'vehicles': vehicles,
    })
    
def tickets(request):
    return render(request, add_vehicles/'tickets.html')
    
def signup(request):
    if request.method == 'POST': 
        form = SignupForm(request.POST)
        
     if form.is_valid(): 
        form.save()  
        return redirect('/login/')  
     else:
     form = SignupForm()
    return render(request, add_vehicles/'signup.html', {
          'form': form
    }) 