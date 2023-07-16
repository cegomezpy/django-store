from django import forms

class quantityForm(forms.Form):
    quantity = forms.IntegerField(label = None, max_value=9999999)