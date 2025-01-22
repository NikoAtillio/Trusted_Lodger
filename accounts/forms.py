from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from .models import User, Profile, RoomListing, Message
from datetime import datetime

class CustomSignupForm(SignupForm):
    user_type = forms.ChoiceField(
        choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')],
        widget=forms.RadioSelect,
        label="I am a"
    )

    def save(self, request):
        user = super().save(request)
        user.user_type = self.cleaned_data['user_type']
        user.save()
        return user

class UserRegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    user_type = forms.ChoiceField(
        choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')],
        widget=forms.RadioSelect,
        label="I am a"
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    dob_day = forms.IntegerField(min_value=1, max_value=31, required=True)
    dob_month = forms.IntegerField(min_value=1, max_value=12, required=True)  # Added missing month field
    dob_year = forms.IntegerField(min_value=1900, max_value=datetime.now().year, required=True)
    user_status = forms.MultipleChoiceField(
        choices=[('looking_for_share', 'I am looking for a flat or house share'),
                 ('have_share', 'I have a flat or house share'),
                 ('find_people', 'I\'d like to find people to form a new share')],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'gender', 'dob_day', 'dob_month', 'dob_year', 'user_status', 'profile_picture']

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
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'living_preferences': forms.Textarea(attrs={'rows': 4}),
        }

class RoomListingForm(forms.ModelForm):
    class Meta:
        model = RoomListing
        fields = ['title', 'description', 'room_type', 'price', 'location', 'postcode', 'available_from', 'minimum_stay', 'bills_included']
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
