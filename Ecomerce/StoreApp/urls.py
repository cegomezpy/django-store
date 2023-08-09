from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name = 'Search'),
    path('<str:header>/', views.store, name = 'Store'), 
    path('filter/<str:header>/', views.filter, name = 'Filter'),
]