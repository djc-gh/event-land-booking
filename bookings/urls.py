from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_availability, name='search_availability'),
    path('book/<int:land_id>/', views.booking_form, name='booking_form'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('calendar/<int:land_id>/', views.land_availability_calendar, name='land_availability_calendar'),
]
