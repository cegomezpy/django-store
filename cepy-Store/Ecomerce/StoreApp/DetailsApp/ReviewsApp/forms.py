from django import forms
from .models import Review

class ReviewForm(forms.Form):
    rating = forms.IntegerField(max_value=5, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id':'product-rating', 'type':'hidden'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'cols':30, 'rows':5}))

    class Meta:
        model = Review
        fields = ['rating', 'text_area']