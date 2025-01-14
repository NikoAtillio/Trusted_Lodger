from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_matches')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='landlord_matches')
    room_listing = models.ForeignKey('listings.RoomListing', on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Match: {self.tenant.username} with {self.landlord.username} for {self.room_listing.title}'