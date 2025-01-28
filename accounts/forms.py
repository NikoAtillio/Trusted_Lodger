from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from datetime import datetime, date
from .models import User, Profile, RoomListing, RoomImage, Message
from django.core.validators import RegexValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import logging
from django import forms
from .models import RoomListing, RoomImage
from django.core.validators import FileExtensionValidator


logger = logging.getLogger(__name__)


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
    # Define choices at class level
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    USER_STATUS_CHOICES = [
        ('offered', 'I have a room to rent'),
        ('wanted', 'I am looking for a room'),
        ('coliving', 'I am interested in co-living'),
    ]

    user_type = forms.ChoiceField(
        choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')],
        widget=forms.RadioSelect,
        label="I am a",
        required=True,
        error_messages={'required': 'Please select whether you are a tenant or landlord'}
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        error_messages={'required': 'Please select your gender'}
    )

    dob_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        required=True,
        error_messages={
            'required': 'Please enter a valid day',
            'min_value': 'Day must be between 1 and 31',
            'max_value': 'Day must be between 1 and 31'
        }
    )

    dob_month = forms.IntegerField(
        min_value=1,
        max_value=12,
        required=True,
        error_messages={
            'required': 'Please enter a valid month',
            'min_value': 'Month must be between 1 and 12',
            'max_value': 'Month must be between 1 and 12'
        }
    )

    dob_year = forms.IntegerField(
        min_value=1900,
        max_value=datetime.now().year - 17,
        required=True,
        error_messages={
            'required': 'Please enter a valid year',
            'min_value': 'Year must be 1900 or later',
            'max_value': 'You must be at least 17 years old'
        }
    )

    user_status = forms.MultipleChoiceField(
        choices=USER_STATUS_CHOICES,  # Changed from Meta.USER_STATUS_CHOICES
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Please select at least one option'}
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password1', 'password2',
            'user_type', 'gender', 'dob_day', 'dob_month', 'dob_year',
            'user_status', 'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("The file is too large. Maximum size is 5 MB.")
            if not picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("File type not supported. Please upload a PNG or JPG image.")
        return picture

    def clean(self):
        cleaned_data = super().clean()
        dob_day = cleaned_data.get('dob_day')
        dob_month = cleaned_data.get('dob_month')
        dob_year = cleaned_data.get('dob_year')

        if all([dob_day, dob_month, dob_year]):
            try:
                dob = datetime(dob_year, dob_month, dob_day)
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 17:
                    raise ValidationError('You must be at least 17 years old to register.')
            except ValueError:
                raise ValidationError('Please enter a valid date of birth.')

        user_status = cleaned_data.get('user_status')
        if not user_status:
            raise ValidationError('Please select at least one status option.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('user_status'):
            user.user_status = ','.join(self.cleaned_data['user_status'])
        if commit:
            user.save()
        return user


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'personality_type', 'living_preferences']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'living_preferences': forms.Textarea(attrs={'rows': 4}),
        }


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=UserRegistrationForm.GENDER_CHOICES)
    dob_day = forms.IntegerField(min_value=1, max_value=31)
    dob_month = forms.IntegerField(min_value=1, max_value=12)
    dob_year = forms.IntegerField(min_value=1900, max_value=datetime.now().year)
    user_status = forms.MultipleChoiceField(
        choices=UserRegistrationForm.USER_STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = [
            'bio', 'location', 'personality_type', 'living_preferences',
            'occupation', 'availability', 'budget'
        ]

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
            if self.instance.user.user_status:
                self.fields['user_status'].initial = self.instance.user.user_status.split(',')

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 5 MB )")
            if not picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Unsupported file type")
        return picture

    def clean(self):
        cleaned_data = super().clean()
        dob_day = cleaned_data.get('dob_day')
        dob_month = cleaned_data.get('dob_month')
        dob_year = cleaned_data.get('dob_year')

        if all([dob_day, dob_month, dob_year]):
            try:
                dob = datetime(dob_year, dob_month, dob_day)
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 17:
                    raise ValidationError('You must be at least 17 years old.')
            except ValueError:
                raise ValidationError('Invalid date of birth.')
        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.dob_day = self.cleaned_data['dob_day']
        user.dob_month = self.cleaned_data['dob_month']
        user.dob_year = self.cleaned_data['dob_year']

        if 'user_status' in self.cleaned_data and self.cleaned_data['user_status']:
            user.user_status = ','.join(self.cleaned_data['user_status'])

        if self.cleaned_data.get('profile_picture'):
            user.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user.save()
            profile.save()

        return profile


class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ['image']

    def clean_image(self):
        """Validate a single uploaded image."""
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError('No image uploaded.')

        allowed_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_types:
            raise forms.ValidationError(f'File type not supported: {image.content_type}')
        if image.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError('File size exceeds 5MB.')

        return image
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        
class RoomListingForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, label="Listing Title")
    location = forms.CharField(max_length=100, required=True, label="Location")
    postcode = forms.CharField(max_length=10, required=True, label="Postcode")
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="Price (£/monthly)")
    size = forms.CharField(max_length=50, required=True, label="Size (e.g., 12x15 ft)")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Description")
    available_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Available From")
    minimum_term = forms.IntegerField(min_value=1, required=True, label="Minimum Term (months)")
    maximum_term = forms.IntegerField(min_value=1, required=False, label="Maximum Term (months)")
    deposit = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="Deposit (£)")
    bills_included = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=True, label="Bills Included?")    
    furnishings = forms.CharField(max_length=100, required=False, label="Furnishings")
    parking = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Parking")    
    garden = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Garden/Patio")
    balcony = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Balcony/Roof Terrace")
    disabled_access = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Disabled Access")
    living_room = forms.ChoiceField(choices=[('shared', 'Shared'), ('private', 'Private')], required=False, label="Living Room")
    broadband = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Broadband Included")
    current_household = forms.IntegerField(min_value=1, required=True, label="Current Household")
    total_rooms = forms.IntegerField(min_value=1, required=True, label="Total # Rooms")
    ages = forms.CharField(max_length=50, required=True, label="Ages")
    smoker = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Smoker?")
    pets = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Any Pets?")
    occupation = forms.CharField(max_length=100, required=True, label="Occupation")
    gender = forms.CharField(max_length=50, required=True, label="Gender")
    couples_ok = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Couples OK?")
    smoking_ok = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Smoking OK?")
    pets_ok = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="Pets OK?")
    occupation_preference = forms.CharField(max_length=100, required=False, label="Preferred Occupation")
    references_required = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, label="References Required?")    
    min_age = forms.IntegerField(min_value=18, required=True, label="Min Age")
    max_age = forms.IntegerField(min_value=18, required=True, label="Max Age")

    class Meta:
        model = RoomListing
        fields = [
            'title', 'location', 'postcode', 'price', 'size', 'description',
            'available_from', 'minimum_term', 'maximum_term', 'deposit',
            'bills_included', 'furnishings', 'parking', 'garden', 'balcony',
            'disabled_access', 'living_room', 'broadband', 'current_household',
            'total_rooms', 'ages', 'smoker', 'pets', 'occupation', 'gender',
            'couples_ok', 'smoking_ok', 'pets_ok', 'occupation_preference',
            'references_required', 'min_age', 'max_age'
        ]
        exclude = ['owner', 'created_at', 'updated_at', 'availability']

    def clean_available_from(self):
        available_from = self.cleaned_data.get('available_from')
        if available_from and available_from < datetime.now().date():
            raise ValidationError("The available from date cannot be in the past.")
        return available_from

    def clean(self):
        cleaned_data = super().clean()
        minimum_term = cleaned_data.get('minimum_term')
        maximum_term = cleaned_data.get('maximum_term')

        if maximum_term and minimum_term and maximum_term < minimum_term:
            raise ValidationError("Maximum term cannot be less than minimum term.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('available_from'):
            instance.available_from = self.cleaned_data['available_from']
        if commit:
            instance.save()
        return instance
