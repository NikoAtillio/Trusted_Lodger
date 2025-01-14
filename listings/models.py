from django.db import models
from django.contrib.auth.models import User

class RoomListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_type = models.CharField(max_length=100)  # Add this field
    location = models.CharField(max_length=255)   # Add this field
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Add this field
    
    def __str__(self):
        return self.title
