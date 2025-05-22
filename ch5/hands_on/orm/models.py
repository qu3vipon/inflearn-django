import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def with_image(self):
        return super().get_queryset().filter(image__isnull=False)


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    job = models.CharField(max_length=32, default="developer")
