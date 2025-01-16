from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User  # Import User from accounts app

ROOM_TYPES = [
    ('Single', 'Single Room'),
    ('Double', 'Double Room'),
    ('Ensuite', 'Ensuite Room'),
    ('Studio', 'Studio'),
]

class RoomListing(models.Model):
    """Model for room listings"""
    owner = models.ForeignKey(
        User,
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
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional useful fields
    postcode = models.CharField(max_length=10, blank=True)
    available_from = models.DateField(null=True, blank=True)
    minimum_stay = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Minimum stay in months"
    )
    bills_included = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Room Listing"
        verbose_name_plural = "Room Listings"

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

    # Additional useful fields
    subject = models.CharField(max_length=200, blank=True)
    related_listing = models.ForeignKey(
        RoomListing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.save()