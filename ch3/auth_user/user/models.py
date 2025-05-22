from django.contrib.auth.models import AbstractUser
from django.db import  models

class CustomUser(AbstractUser):
    social_provider = models.CharField(max_length=8, null=True)
