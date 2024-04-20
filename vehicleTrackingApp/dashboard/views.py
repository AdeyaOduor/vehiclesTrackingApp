from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from vehicles.models import vehicles

@login_required
def index(request):
    vehicles = vehicles.objects.filter(created_by=request.user)
    
    return render(request, 'dashboard/index.html',{
          'vehicles': vehicles,
    })