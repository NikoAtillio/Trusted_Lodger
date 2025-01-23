from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from .models import User, Profile, RoomListing, Message
from datetime import datetime
from django.contrib.auth import get_user_model

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

User = get_user_model()

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
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    dob_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        required=True
    )
    dob_month = forms.IntegerField(
        min_value=1,
        max_value=12,
        required=True
    )
    dob_year = forms.IntegerField(
        min_value=1900,
        max_value=datetime.now().year,
        required=True
    )
    user_status = forms.MultipleChoiceField(
        choices=[
            ('looking_for_share', 'I am looking for a flat or house share'),
            ('have_share', 'I have a flat or house share'),
            ('find_people', 'I\'d like to find people to form a new share')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    profile_picture = forms.ImageField(required=False)
    occupation = forms.CharField(required=False, max_length=100)
    availability = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    budget = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password1', 'password2',
            'user_type', 'gender', 'dob_day', 'dob_month', 'dob_year',
            'user_status', 'profile_picture', 'occupation', 'availability', 'budget'
        ]


    def clean(self):
        cleaned_data = super().clean()
        dob_day = cleaned_data.get('dob_day')
        dob_month = cleaned_data.get('dob_month')
        dob_year = cleaned_data.get('dob_year')

        if dob_day and dob_month and dob_year:
            try:
                dob = datetime(dob_year, dob_month, dob_day)
                if (datetime.now() - dob).days < 6570:  # 18 years in days
                    raise forms.ValidationError("You must be at least 18 years old.")
            except ValueError:
                raise forms.ValidationError("Please enter a valid date.")

        user_status = cleaned_data.get('user_status')
        if not user_status:
            raise forms.ValidationError("Please select at least one status option.")

        return cleaned_data  # This returns the cleaned data, preserving user input

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("The file is too large. Maximum size is 5 MB.")

            file_name = picture.name.lower()
            if not file_name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("File type not supported. Please upload a PNG or JPG image.")
        return picture

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'personality_type', 'living_preferences']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'living_preferences': forms.Textarea(attrs={'rows': 4}),
        }

class ProfileEditForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    dob_day = forms.IntegerField(min_value=1, max_value=31)
    dob_month = forms.IntegerField(min_value=1, max_value=12)
    dob_year = forms.IntegerField(min_value=1900, max_value=datetime.now().year)
    user_status = forms.MultipleChoiceField(
        choices=[
            ('looking_for_share', 'I am looking for a flat or house share'),
            ('have_share', 'I have a flat or house share'),
            ('find_people', 'I\'d like to find people to form a new share')
        ],
        widget=forms.CheckboxSelectMultiple,
    )
    budget = forms.DecimalField(required=False)
    occupation = forms.CharField(required=False)
    availability = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'personality_type', 'living_preferences']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['gender'].initial = self.instance.user.gender
            self.fields['dob_day'].initial = self.instance.user.dob_day
            self.fields['dob_month'].initial = self.instance.user.dob_month
            self.fields['dob_year'].initial = self.instance.user.dob_year
            self.fields['user_status'].initial = self.instance.user.user_status.split(',') if self.instance.user.user_status else []

    def clean(self):
        cleaned_data = super().clean()
        dob_day = cleaned_data.get('dob_day')
        dob_month = cleaned_data.get('dob_month')
        dob_year = cleaned_data.get('dob_year')

        if all([dob_day, dob_month, dob_year]):
            try:
                dob = datetime(dob_year, dob_month, dob_day)
                if (datetime.now() - dob).days < 6570:  # 18 years in days
                    raise forms.ValidationError("You must be at least 18 years old.")
            except ValueError:
                raise forms.ValidationError("Please enter a valid date.")

        return cleaned_data

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("The file is too large. Maximum size is 5 MB.")

            file_name = picture.name.lower()
            if not file_name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("File type not supported. Please upload a PNG or JPG image.")
        return picture

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update user fields
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.dob_day = self.cleaned_data['dob_day']
        user.dob_month = self.cleaned_data['dob_month']
        user.dob_year = self.cleaned_data['dob_year']
        user.user_status = ','.join(self.cleaned_data['user_status'])

        if commit:
            user.save()
            profile.save()

        return profile

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