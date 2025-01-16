from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, RoomListing, Message

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                 'password1', 'password2', 'user_type']

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'personality_type', 'living_preferences']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'living_preferences': forms.Textarea(attrs={'rows': 4}),
        }
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'personality_type', 'living_preferences']

class RoomListingForm(forms.ModelForm):
    class Meta:
        model = RoomListing
        exclude = ['owner', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }