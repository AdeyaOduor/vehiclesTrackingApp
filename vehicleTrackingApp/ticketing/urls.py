from django.urls import path
from .import views

app_name = 'ticketing'

urlpatterns = [
    path('', views.tickets, name='tickets'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:vehicles_pk>/', views.new_ticketing, name='new'),
]