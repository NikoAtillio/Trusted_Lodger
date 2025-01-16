from django.db import models
from django.conf import settings

class Match(models.Model):
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_matches'
    )
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='landlord_matches'
    )
    room_listing = models.ForeignKey(
        'listings.RoomListing',
        on_delete=models.CASCADE,
        related_name='matches'
    )
    matched_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-matched_at']

    def __str__(self):
        return f'Match: {self.tenant.username} with {self.landlord.username} for {self.room_listing.title}'