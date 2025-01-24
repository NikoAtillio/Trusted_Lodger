from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import User, Profile, RoomListing, Message

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
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'user_type',
            'gender',
            'dob_day',
            'dob_month',
            'dob_year',
            'user_status',
            'profile_picture'
        ]

        GENDER_CHOICES = [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ]

        USER_STATUS_CHOICES = [
            ('looking_for_share', 'I am looking for a flat or house share'),
            ('have_share', 'I have a flat or house share'),
            ('find_people', 'I\'d like to find people to form a new share')
        ]

    user_type = forms.ChoiceField(
        choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')],
        widget=forms.RadioSelect,
        label="I am a",
        required=True,
        error_messages={'required': 'Please select whether you are a tenant or landlord'}
    )

    gender = forms.ChoiceField(
        choices=Meta.GENDER_CHOICES,
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
        choices=Meta.USER_STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Please select at least one option'}
    )

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
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise ValidationError("The file is too large. Maximum size is 5 MB.")
            if not picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("File type not supported. Please upload a PNG or JPG image.")
        return picture

    def clean(self):
        cleaned_data = super().clean()

        # Validate date of birth
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

        # Validate user status
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
    gender = forms.ChoiceField(choices=UserRegistrationForm.Meta.GENDER_CHOICES)
    dob_day = forms.IntegerField(min_value=1, max_value=31)
    dob_month = forms.IntegerField(min_value=1, max_value=12)
    dob_year = forms.IntegerField(min_value=1900, max_value=datetime.now().year)
    user_status = forms.MultipleChoiceField(
        choices=UserRegistrationForm.Meta.USER_STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = [
            'bio',
            'location',
            'personality_type',
            'living_preferences',
            'occupation',
            'availability',
            'budget'
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

class RoomListingForm(forms.ModelForm):
    class Meta:
        model = RoomListing
        fields = [
            'title',
            'description',
            'room_type',
            'price',
            'location',
            'postcode',
            'available_from',
            'minimum_stay',
            'bills_included'
        ]
        exclude = ['owner', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'price': {
                'required': 'Please enter a price',
                'invalid': 'Please enter a valid price'
            },
            'location': {
                'required': 'Please enter a location'
            },
            'postcode': {
                'required': 'Please enter a postcode'
            }
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }