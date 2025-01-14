from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, RoomListing, Message

ROOM_TYPES = [
    ('Single', 'Single Room'),
    ('Double', 'Double Room'),
    ('Ensuite', 'Ensuite Room'),
    ('Studio', 'Studio'),
]

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

class ProfileForm(forms.ModelForm):
    """Form for user profile creation/editing"""
    class Meta:
        model = Profile
        fields = ['bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter your location'
            })
        }

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
                'min': '0'
            })
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

class MessageForm(forms.ModelForm):
    """Form for sending messages"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message here...',
                'class': 'form-control'
            })
        }