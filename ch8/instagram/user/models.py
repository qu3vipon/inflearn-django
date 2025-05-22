from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class CustomUser(AbstractUser):
    email = models.EmailField()

    USERNAME_FIELD = "email"  # 기본 인증에 사용하는 필드를 변경
    REQUIRED_FIELDS = ["username"]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email")
        ]


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name="followings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "follower"], name="unique_follow_relationship")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower_id} -> {self.user_id}"
