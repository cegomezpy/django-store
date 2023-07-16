from django.urls import path
from .views import UserAuth, log_in, log_out


urlpatterns = [
    path('', UserAuth.as_view(), name='Auth'),
    path('login/', log_in, name='Login'),
    path('logout/', log_out, name='Logout'),
]