from django import forms


class CheckoutForm(forms.Form):
    nombre = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'nombre'})
    )
    apellidos = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )
    dirección = forms.CharField(
        label='Address',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Calle 4/1ra y 3ra'})
    )
    email = forms.EmailField(
        required=False,
        label='E-mail',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
    )
    numero_telefonico = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '5355091046'})
        )
