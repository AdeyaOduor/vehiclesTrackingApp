from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from vehicles.models import Vehicle
from .forms import TicketingticketsForm
from .models import Ticketing

@login_required
def new_ticketing(request, vehicles_pk):
    vehicles = get_object_or_404(Vehicle, pk=vehicles_pk)
    if vehicles.created_by == request.user:
        return redirect('dashboard:index')

    ticketing = Ticketing.objects.filter(vehicles=vehicles).filter(members__in=[request.user.id])

    if ticketing:
        return redirect('ticketing:detail', pk=ticketing.first().id)

    if request.method == 'POST':
        form = TicketingticketsForm(request.POST)
        if form.is_valid():
            ticketing = Ticketing.objects.create(vehicles=vehicles)
            ticketing.members.add(request.user)
            ticketing.members.add(vehicles.created_by)
            ticketing.save()

            ticketing_tickets = form.save(commit=False)
            ticketing_tickets.ticketing = ticketing
            ticketing_tickets.created_by = request.user
            ticketing_tickets.save()

            return redirect('vehicles:detail', pk=vehicles_pk)
    else:
        form = TicketingticketsForm()
    return render(request, 'ticketing/new.html', {
        'form': form
    })

@login_required
def ticketing(request):
    ticketing = Ticketing.objects.filter(members__in=[request.user.id])
    return render(request, 'ticketing/tickets.html', {
        'ticketing': ticketing
    })

@login_required
def detail(request, pk):
    ticket = Ticketing.objects.filter(members__in=[request.user.id]).get(pk=pk)
    if request.method == 'POST':
        form = TicketingticketsForm(request.POST)
        if form.is_valid():
            ticketing_ticket = form.save(commit=False)
            ticketing_ticket.ticketing = ticket
            ticketing_ticket.created_by = request.user
            ticketing_ticket.save()
            ticket.save()
            return redirect('ticketing:detail', pk=pk)
    else:
        form = TicketingticketsForm()
    return render(request, 'ticketing/detail.html', {
        'ticketing': ticketing,
        'form': form
    })