from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4

ROOM_TYPES = [
    ('Single', 'Single Room'),
    ('Double', 'Double Room'),
    ('Ensuite', 'Ensuite Room'),
    ('Studio', 'Studio'),
]

class User(AbstractUser):
    """Custom user model for authentication with related names updated"""
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=[('lodger', 'Lodger'), ('homesharer', 'Homesharer')]
    )
    groups = models.ManyToManyField(
        Group,
        related_name='hello_world_users',  # Changed related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hello_world_users_permissions',  # Changed related_name
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Profile(models.Model):
    """User profile for both lodgers and homesharers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile - {self.user.username}"

class RoomListing(models.Model):
    """Model for room listings"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

class Message(models.Model):
    """Model for user messages"""
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"  # Ensured usernames are displayed
