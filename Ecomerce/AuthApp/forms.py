from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from ..UserApp.models import Client
from captcha.fields import ReCaptchaField

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=250, label="Nombre de Usuario", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'joedhon'}))
    nombre = forms.CharField(max_length=250, label="Nombre", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Joe'}))
    email = forms.EmailField(required=False, label="Email(Opcional)", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'somename@email.com'}))
    direccion = forms.CharField(max_length=250, label="Dirección", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Calle1 / 2da y 3ra'}))
    numero_telefonico = forms.CharField(max_length=20, label="Número de móvil", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '5355091046'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label="Repite la Contraseña",widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '********'}))
    prueba_que_eres_humano = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'nombre', 'direccion', 'numero_telefonico', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre']
        client = Client(user=user, direccion=self.cleaned_data['direccion'], numero_telefonico=self.cleaned_data['numero_telefonico'])
        if commit:
            user.save()
            client.save()
        return user

class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=250, label="Nombre de Usuario", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'joedhon'}))
    password = forms.CharField(max_length=250, label="Contraseña", widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '********'}))
    prueba_que_eres_humano = ReCaptchaField()