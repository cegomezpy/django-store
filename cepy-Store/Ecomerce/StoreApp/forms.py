from django import forms
from .models import Category

class PriceForm(forms.Form):
    min_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MIN', 'class':"form-control form-control-sm"}))
    max_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MAX', 'class':"form-control form-control-sm"}))
    
class CategoryForm(forms.Form):
    categorys = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class SearchForm(forms.Form):
    search_bar = forms.CharField(required=False, label=False, widget=forms.TextInput(attrs={'class':'rounded-1 form-control', 'placeholder':'search for products'}))