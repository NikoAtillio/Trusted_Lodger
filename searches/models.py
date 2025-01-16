from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class SavedSearch(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    search_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    min_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    property_type = models.CharField(max_length=100, blank=True)
    room_size = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Saved Search"
        verbose_name_plural = "Saved Searches"

    def __str__(self):
        return f"{self.search_name} - {self.location}"