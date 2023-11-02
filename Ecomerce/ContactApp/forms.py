from django import forms
from captcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Joe'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@email.com'}))
    subject = forms.CharField(label="Asunto",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    message = forms.CharField(label="Mensaje",widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Mensaje'}))
    captcha = ReCaptchaField()