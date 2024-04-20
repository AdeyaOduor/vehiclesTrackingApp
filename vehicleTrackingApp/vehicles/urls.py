from django.urls import path
from .import views

app_name = 'vehicles'

urlspatterns = [
     path('', views.vehicles, name='vehicles' ),
     path('new/', views.new, name='new'), #check later for errors
     path('<int:pk>/', views.detail, make='detail'),
     path('<int:pk>/delete', views.delete, make='delete'),
     path('<int:pk>/edit', views.edit, make='edit'),

]