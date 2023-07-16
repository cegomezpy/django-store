from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='Cart'),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('update_cart/', views.update_cart, name = "update_cart"),
    path('delete_product/', views.delete_product, name = "detele_product"),
]