from django import forms
from captcha.fields import ReCaptchaField


class CheckoutForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Joe'})
    )
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Calle 4/1ra y 3ra'})
    )
    email = forms.EmailField(
        required=False,
        label='E-mail(opcional)',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
    )
    numero_telefonico = forms.CharField(
        label="Número Telefónico",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '5355091046'})
        )
    prueba_que_eres_humano = ReCaptchaField()