from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='profile_images/%Y/%m/%d/', blank=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.username


