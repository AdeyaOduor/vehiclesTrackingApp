from django.urls import path
from .import views

app_name = 'vehicles'

# urlspatterns = [
#      path('', views.vehicles, name='Vehicle' ),
#      path('new/', views.new, name='new'), #check later for errors
#      path('<int:pk>/', views.detail, make='detail'),
#      path('<int:pk>/delete', views.delete, make='delete'),
#      path('<int:pk>/edit', views.edit, make='edit'),

# ]

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('assign-driver/<uuid:vehicle_id>/', views.assign_driver, name='assign_driver'),
    path('submit-ticket/', views.submit_work_ticket, name='submit_ticket'),
    path('submit-fueling/', views.submit_fueling, name='submit_fueling'),
    path('update-location/', views.update_location, name='update_location'),
    path('vehicle-locations/', views.vehicle_locations, name='vehicle_locations'),
]
