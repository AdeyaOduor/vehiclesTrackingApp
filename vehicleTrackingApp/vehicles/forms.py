# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Vehicle, WorkTicket, MaintenanceSchedule, Fueling

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'county', 'subcounty', 'phone_number')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude = ['current_driver']

# class NewVehiclesForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ('category', 'make', 'description', 'registration', 'image',)
#         widgets = {
#             'category': forms.Select(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'make': forms.TextInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'registration': forms.TextInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'image': forms.FileInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#         }

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

class EditVehiclesForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('make', 'description', 'registration', 'image', 'is_ticketed',)
        widgets = {
            'make': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'registration': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
