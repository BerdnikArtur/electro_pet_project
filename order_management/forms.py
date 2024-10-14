from django import forms
from .models import *

class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'telephone']
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'State'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Country'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'ZIP Code'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Telephone'}))