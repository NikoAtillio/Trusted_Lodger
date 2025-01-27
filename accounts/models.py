from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator, EmailValidator, FileExtensionValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from PIL import Image

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
    
    def get_age(self):
        """Calculate user's age based on DOB fields"""
        if all([self.dob_year, self.dob_month, self.dob_day]):
            try:
                dob = datetime(self.dob_year, self.dob_month, self.dob_day)
                today = datetime.now()
                return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            except:
                return None
        return None

    def get_full_name(self):
        """Return full name or email if name not set"""
        full_name = super().get_full_name()
        return full_name if full_name else self.email

    @property
    def profile_picture_url(self):
        """Return profile picture URL or None"""
        try:
            return self.profile_picture.url
        except:
            return None

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
    title = models.CharField(max_length=200, default="Room Available")
    description = models.TextField(default="Room description not provided")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)
    location = models.CharField(max_length=255, default="Location not specified")
    postcode = models.CharField(max_length=10, default="Not specified")

    # Room Details
    size = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Double', 'Double'), ('single', 'single'), ('double', 'double')], default='Single')    
    availability = models.CharField(max_length=100, default="Immediately")
    minimum_term = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    maximum_term = models.IntegerField(null=True, blank=True, default=12)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bills_included = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    furnishings = models.CharField(max_length=255, default="Not specified")

    # Property Features
    parking = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    garden = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    balcony = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    disabled_access = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    living_room = models.CharField(max_length=7, choices=LIVING_ROOM_CHOICES, default='shared')
    broadband = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no') 

    # Household Details
    current_household = models.IntegerField(default=1)
    total_rooms = models.IntegerField(default=1)
    ages = models.CharField(max_length=100, default="18-99")
    smoker = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    pets = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    occupation = models.CharField(max_length=100, default="Not specified")
    gender = models.CharField(max_length=50, default="Any")

    # Preferences
    couples_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    smoking_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    pets_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='no')
    occupation_preference = models.CharField(max_length=100, default="Any")
    references_required = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='yes')
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=99)


    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"
    
    def get_main_image(self):
        """Returns the URL of the first image of the listing or None"""
        main_image = self.images.first()
        return main_image.image_url if main_image else None

    def get_image_count(self):
        """Returns the number of images for this listing"""
        return self.images.count()

    def is_available(self):
        """Check if the room is currently available"""
        try:
            availability_date = datetime.strptime(self.availability, '%Y-%m-%d').date()
            return availability_date >= timezone.now().date()
        except:
            return False

    def clean(self):
        """Validate model data"""
        from django.core.exceptions import ValidationError

        if self.min_age > self.max_age:
            raise ValidationError('Minimum age cannot be greater than maximum age')

        if self.minimum_term and self.maximum_term:
            if self.minimum_term > self.maximum_term:
                raise ValidationError('Minimum term cannot be greater than maximum term')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class RoomImage(models.Model):
    room_listing = models.ForeignKey('RoomListing', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='room_images/',
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
        ]
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"

    def __str__(self):
        return f"Image {self.order} for {self.room_listing}"

    def save(self, *args, **kwargs):
        if not self.pk and self.room_listing:
            last_order = RoomImage.objects.filter(
                room_listing=self.room_listing
            ).aggregate(models.Max('order'))['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img = img.convert('RGB')  # Ensure compatibility
            img.thumbnail((800, 800))  # Resize to max 800x800
            img.save(self.image.path, quality=85)  # Save with reduced quality

    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return None
        
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
