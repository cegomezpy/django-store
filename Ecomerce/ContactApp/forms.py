from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(label="Asunto",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(label="Mensaje",widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Message'}))
