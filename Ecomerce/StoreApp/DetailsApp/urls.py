from django.urls import path
from . import views

urlpatterns = [
    path('<str:header>/<int:product_id>/', views.details, name='Details'),
]