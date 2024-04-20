from django import forms
from .models import Ticketingtickets

class TicketingticketsForm(forms.ModelForm)
     class Meta:
         model = Ticketingtickets
         fields = ('origin','departure_date','destination','milage_km','return_date',)
         widgets = {
             'origin': forms.CharField(attrs{
                 'class': 'py 2 px-3 rounded-xl border'
             })
              'departure_date': forms.CharField(attrs{
                 'class': 'py 2 px-3 rounded-xl border'
             })
              'destination': forms.CharField(attrs{
                 'class': 'py 2 px-3 rounded-xl border'
             })
              'milage_km': forms.CharField(attrs{
                 'class': 'py 2 px-3 rounded-xl border'
             })
              'return_date': forms.CharField(attrs{
                 'class': 'py 2 px-3 rounded-xl border'
             })
             
         }