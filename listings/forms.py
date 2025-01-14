from django import forms
from .models import RoomListing

ROOM_TYPES = [
    ('Single', 'Single Room'),
    ('Double', 'Double Room'),
    ('Ensuite', 'Ensuite Room'),
    ('Studio', 'Studio'),
]

class RoomListingForm(forms.ModelForm):
    """Form for creating/editing room listings"""
    class Meta:
        model = RoomListing
        fields = [
            'title',
            'description',
            'room_type',
            'price',
            'location',
            'available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the room and amenities...'
            }),
            'room_type': forms.Select(choices=ROOM_TYPES),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter price'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter room location'
            }),
        }

class SearchForm(forms.Form):
    """Form for searching room listings"""
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter location...'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min price'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max price'
        })
    )
    room_type = forms.ChoiceField(
        choices=[('', 'All')] + list(ROOM_TYPES),
        required=False
    )