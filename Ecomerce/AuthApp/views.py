from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.
class UserAuth(View):
    # If GET request
    def get(self, request):
        # Create empty form
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'creationForm':form})
    # If POST request
    def post(self, request):
        # Create User Form with request data
        form = CustomUserCreationForm(request.POST)
        # If form is valid
        if form.is_valid():
            # Register and login the user
            user = form.save()
            login(request, user)
            # Redirect the user to Store
            return redirect('Home')
        # If form is not valid
        else:
            # Get all error messages
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, 'register.html', {'creationForm':form})
# Logout function
def log_out(request):
    logout(request)
    return redirect('Home')
# Login function
def log_in(request):
    form = CustomUserAuthenticationForm()
    # If POST request
    if request.method == 'POST':
        # Pass request data to form
        form = CustomUserAuthenticationForm(request, data=request.POST)
        # If form is valid
        if form.is_valid():
            # get clean data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate user
            auth = authenticate(username=username, password=password)
            # Redirect to Store if user is succesfully authenticated
            if auth:
                login(request, auth)
                return redirect('Home')
        # If request data not valid get all error messages
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    # If not POST return empty form with errors
    for msg in form.error_messages:
        messages.error(request, form.error_messages[msg])
    return render(request, 'login.html', {'form':form})
