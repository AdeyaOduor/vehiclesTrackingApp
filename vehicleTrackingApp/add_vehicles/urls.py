from django.contrib.auth import views as auth_views
from django.urls import path
from .import views
from .forms import LoginForm

app_name = 'add_vehicles'

urlspatterns = [
     path('', views.index, name='index'),
     path('tickets/',views.tickets, name='tickets'),
     path('signup/',views.signup, name='signup'),
     path('login/', auth_views.LoginView.as_view(template_name='add_vehicles/login.html', authentication_form=LoginForm), name='login'),
]