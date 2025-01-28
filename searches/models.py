from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import RoomListing

class PropertySearch(models.Model):
    """Model to store search parameters and results"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    search_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    search_type = models.CharField(
        max_length=20,
        choices=[
            ('offered', 'Rooms for Rent'),
            ('wanted', 'Rooms Wanted'),
            ('coliving', 'CoLiving Search')
        ]
    )
    property_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('Flat', 'Flat'),
            ('House', 'House'),
            ('Studio', 'Studio')
        ]
    )
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    room_size = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('Single', 'Single'),
            ('Double', 'Double')
        ]
    )
    availability_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Property searches"
        ordering = ['-search_date']

    def __str__(self):
        return f"Search by {self.user or 'Anonymous'} - {self.location} ({self.search_date.date()})"

