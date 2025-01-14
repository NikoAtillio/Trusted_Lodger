from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Profile  # Correctly import the Profile model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with additional fields."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """Override save method to include email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    class Meta:
        model = Profile  # Use the imported Profile model directly
        fields = ('bio', 'location')
