from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'first_name'})
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'last_name'})
    )
    address = forms.CharField(
        label='Address',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Street #99/Street1 and Street2'})
    )
    email = forms.EmailField(
        required=False,
        label='E-mail',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '5355091046'})
        )
