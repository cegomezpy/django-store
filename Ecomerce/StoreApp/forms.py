from django import forms
from .models import Category, Events, Product

class PriceForm(forms.Form):
    min_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MIN', 'class':"form-control form-control-sm"}), max_value=999999)
    max_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MAX', 'class':"form-control form-control-sm"}), max_value=999999)
    
class CategoryForm(forms.Form):
    query = Category.objects.all().filter(products__in=Product.objects.all()).distinct()
    categories = forms.ModelMultipleChoiceField(
        required=False,
        queryset=query,
        widget=forms.CheckboxSelectMultiple(attrs={'class':"d-inline"})
    )

class CategoryEventsForm(forms.Form):
    query = Category.objects.all().filter(events__in=Events.objects.all()).distinct()
    categories = forms.ModelMultipleChoiceField(
        required=False,
        queryset=query,
        widget=forms.CheckboxSelectMultiple(attrs={'class':"d-inline"})
    )

class SearchForm(forms.Form):
    search_bar = forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={'class':'rounded-1 form-control', 'placeholder':'Buscar productos'}))