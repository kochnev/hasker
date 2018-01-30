from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Model representing a userprofile (additional info about user) """
    user = models.OneToOneField(User, related_name='profile')

    avatar = models.ImageField(upload_to='profile_images/%Y/%m/%d/', blank=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.user.username

