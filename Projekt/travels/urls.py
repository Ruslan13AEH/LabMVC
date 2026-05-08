from django.urls import path
from . import views

urlpatterns = [
    # Trips
    path('', views.trip_list, name='trip_list'),
    path('trips/new/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:pk>/edit/', views.trip_edit, name='trip_edit'),
    path('trips/<int:pk>/delete/', views.trip_delete, name='trip_delete'),

    # Travelers
    path('travelers/', views.traveler_list, name='traveler_list'),
    path('travelers/new/', views.traveler_create, name='traveler_create'),
    path('travelers/<int:pk>/edit/', views.traveler_edit, name='traveler_edit'),
    path('travelers/<int:pk>/delete/', views.traveler_delete, name='traveler_delete'),

    # Reservations
    path('trips/<int:trip_pk>/reservations/new/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
]
