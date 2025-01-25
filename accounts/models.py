from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'landlord')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    )
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    username = None  # Remove username field
    email = models.EmailField(unique=True, validators=[EmailValidator()])  # Set email as unique and required

    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    dob_day = models.IntegerField(null=True, blank=True)
    dob_month = models.IntegerField(null=True, blank=True)
    dob_year = models.IntegerField(null=True, blank=True)
    user_status = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Set email as the USERNAME_FIELD
    REQUIRED_FIELDS = []  # Remove required username

    @property
    def is_landlord(self):
        return self.user_type == 'landlord'

    @property
    def is_tenant(self):
        return self.user_type == 'tenant'

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    personality_type = models.CharField(max_length=100, blank=True)
    living_preferences = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    availability = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.email}'s profile"

class RoomListing(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Ensuite', 'Ensuite Room'),
        ('Studio', 'Studio'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    LIVING_ROOM_CHOICES = [
        ('shared', 'Shared'),
        ('private', 'Private'),
    ]

    # Basic Information
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    # Room Details
    size = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    minimum_term = models.IntegerField(validators=[MinValueValidator(1)])
    maximum_term = models.IntegerField(null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    bills_included = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    furnishings = models.CharField(max_length=255)

    # Property Features
    parking = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    garden = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    balcony = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    disabled_access = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    living_room = models.CharField(max_length=7, choices=LIVING_ROOM_CHOICES)
    broadband = models.CharField(max_length=3, choices=YES_NO_CHOICES)

    # Household Details
    current_household = models.IntegerField()
    total_rooms = models.IntegerField()
    ages = models.CharField(max_length=100)
    smoker = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    pets = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    occupation = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)

    # Preferences
    couples_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    smoking_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    pets_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    occupation_preference = models.CharField(max_length=100)
    references_required = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    # Images
    images = models.ManyToManyField('RoomImage', related_name='room_listings', blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"

class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.subject

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
