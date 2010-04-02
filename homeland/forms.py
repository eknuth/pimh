from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(max_length=255)


class SearchForm(forms.Form):
    coords = forms.CharField(max_length=255)
