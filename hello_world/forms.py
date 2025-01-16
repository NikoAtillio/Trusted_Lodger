from django import forms

class HomeSearchForm(forms.Form):
    """Form for the homepage initial search"""
    SEARCH_TYPES = [
        ('rooms', 'Rooms'),
        ('tenants', 'Tenants'),
        ('coliving', 'CoLiving')
    ]

    location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter a location...',
            'class': 'form-control search-input',
            'id': 'location-search'
        })
    )

    search_type = forms.ChoiceField(
        choices=SEARCH_TYPES,
        widget=forms.RadioSelect(attrs={
            'class': 'search-type-radio',
            'id': 'search-type'
        })
    )

class ContactForm(forms.Form):
    """Form for the contact page"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your first name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your last name'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message',
            'rows': 5
        })
    )
