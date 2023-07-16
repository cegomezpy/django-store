from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='Store'), 
    path('filter/', views.filter, name='Filter'),
]