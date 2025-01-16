import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class SocialProviderChoice(models.TextChoices):
    KAKAO = "kakao", "Kakao"
    NAVER = "naver", "Naver"
    GOOGLE = "google", "Google"


class User(AbstractUser):
    models.PositiveIntegerField
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    social_provider = models.CharField(
        choices=SocialProviderChoice.choices, max_length=8, null=True
    )


class ProfileManager(models.Manager):
    def with_image(self):
        return super().get_queryset().filter(image__isnull=False)


# 1:1
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', null=True)
    preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성할 때만 한 번 저장
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 마다 변경

    objects = ProfileManager()


# 1:N
class Order(models.Model):
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# N:M
class Project(models.Model):
    name = models.CharField(max_length=20)
#     users = models.ManyToManyField(User, through="ProjectUser")
#
#
# class ProjectUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = "django_orm_project_user"


class UserProjectRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
