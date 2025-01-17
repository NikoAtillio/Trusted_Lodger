from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator

class User(AbstractUser):
    USER_TYPES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    personality_type = models.CharField(max_length=100, blank=True)
    living_preferences = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class RoomListing(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Ensuite', 'Ensuite Room'),
        ('Studio', 'Studio'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_listings')  # Updated related_name
    title = models.CharField(max_length=200)
    description = models.TextField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='Single')
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Room Listing"
        verbose_name_plural = "Room Listings"

    def __str__(self):
        return f"{self.title} - {self.location}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"