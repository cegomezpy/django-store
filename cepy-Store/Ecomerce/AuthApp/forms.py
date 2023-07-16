from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from ..UserApp.models import Client

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    email = forms.EmailField()
    address = forms.CharField(max_length=250)
    mobile_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'address', 'mobile_number', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        client = Client(user=user, address=self.cleaned_data['address'], mobile_number=self.cleaned_data['mobile_number'])
        if commit:
            user.save()
            client.save()
        return user