from django import forms
from .models import Vehicle

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewVehiclesForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('category', 'make', 'description', 'registration', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
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