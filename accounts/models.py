from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class User(AbstractUser):
    """Custom user model for authentication with related names updated"""
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=[('lodger', 'Lodger'), ('homesharer', 'Homesharer')]
    )
    groups = models.ManyToManyField(
        Group,
        related_name='accounts_users',  # Changed related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_users_permissions',  # Changed related_name
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Profile(models.Model):
    """User profile for both lodgers and homesharers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)  # Made location optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile - {self.user.username}"
