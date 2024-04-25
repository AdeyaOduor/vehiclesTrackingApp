from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your personal number',
        'class': 'w-full py-4 rounded-xl',                
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password',
        'class': 'w-full py-4 rounded-xl',                
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'national_id', 'password1', 'password2')
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your personal number',
        'class': 'w-full py-4 rounded-xl',                
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'your email address',
        'class': 'w-full py-4 rounded-xl',                
    }))
    national_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your national id',
        'class': 'w-full py-4 rounded-xl',                
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password1',
        'class': 'w-full py-4 rounded-xl',                
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'repeat password',
        'class': 'w-full py-4 rounded-xl',                
    }))