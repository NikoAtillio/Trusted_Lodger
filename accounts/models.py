from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'landlord')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)

    objects = CustomUserManager()

    @property
    def is_landlord(self):
        return self.user_type == 'landlord'

    @property
    def is_tenant(self):
        return self.user_type == 'tenant'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    personality_type = models.CharField(max_length=100, blank=True)
    living_preferences = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s profile"

class RoomListing(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Ensuite', 'Ensuite Room'),
        ('Studio', 'Studio'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='room_listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        default='Single'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10, blank=True)
    available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    minimum_stay = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Minimum stay in months"
    )
    bills_included = models.BooleanField(default=False)
    amenities = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated list of amenities (e.g., 'WiFi, Parking, Pool')"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Room Listing"
        verbose_name_plural = "Room Listings"

    def __str__(self):
        return f"{self.title} - {self.location}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('room_listing_detail', args=[str(self.id)])

    def get_amenities_list(self):
        """Returns a list of amenities"""
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []

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
        return f"Message from {self.sender} to {self.recipient}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()