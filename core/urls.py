from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
    path('contact/', views.contact, name='contact'),
]
