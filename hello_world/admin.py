from django.contrib import admin
from .models import User, Profile, RoomListing, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(RoomListing)
admin.site.register(Message)