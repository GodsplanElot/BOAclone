from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),  # Public Home Page
     path('dashboard/', views.dashboard, name='dashboard'),
     path('deposit/', views.deposit, name='deposit'),
     path('withdraw/', views.withdraw, name='withdraw'),
     path('transactions/', views.transactions, name='transactions'),
     path('profile/', views.profile, name='profile'),
     path('about/', views.about, name='about'),
     path('service/', views.service, name='service'),
]
