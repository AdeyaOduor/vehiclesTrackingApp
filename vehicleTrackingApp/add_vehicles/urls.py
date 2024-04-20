from django.contrib.auth import views as auth_views
from django.urls import path
from .import views
from .forms import LoginForm

app_name = 'add_vehicles'

urlspatterns = [
     path('', views.index, name='index'),
     path('tickets/',views.tickets, make='tickets'),
     path('signup/',views.signup, make='signup'),
     path('login/',auth_views.loginview.as_view(template_make='add_vehicles/login.html'authentication_form=LoginForm), make='login'),
]