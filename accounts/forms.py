from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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
        model = 'accounts.Profile'  # Use string reference to avoid circular import
        fields = ('bio', 'location')  # Ensure 'birth_date' is NOT included