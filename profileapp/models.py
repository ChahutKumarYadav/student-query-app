from django.db import models

from account.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    institute = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)


class About(models.Model):
    user = models.OneToOneField(User, related_name="user_about", on_delete=models.CASCADE)
    about = models.TextField(max_length=2000, blank=True, null=True)
