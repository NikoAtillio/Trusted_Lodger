from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class SavedSearch(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    search_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    min_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    property_type = models.TextField(blank=True, help_text="Comma-separated list of property types")
    room_size = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amenities = models.TextField(blank=True, null=True, help_text="Comma-separated list of amenities")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Saved Search"
        verbose_name_plural = "Saved Searches"

    def __str__(self):
        return f"{self.search_name} - {self.location}"
class SavedAd(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        verbose_name = "Saved Ad"
        verbose_name_plural = "Saved Ads"

    def __str__(self):
        return f'{self.user.email} - {self.ad.title}'
