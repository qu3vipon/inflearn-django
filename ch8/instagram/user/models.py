from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # 사용자의 인증에 사용할 필드를 지정하는 속성
    REQUIRED_FIELDS = ["username"]  # 사용자 생성시 필수로 입력해야 하는 추가 필드를 지정하는 속성


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)  # 팔로우 당하는 사용자
    follower = models.ForeignKey(CustomUser, related_name="followings", on_delete=models.CASCADE)  # 팔로우 하는 사용자
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "follower"], name="unique_follow_relationship")  # 동일한 관계 중복 방지
        ]
        ordering = ["-created_at"]  # 최신 순 정렬

    def __str__(self):
        return f"{self.follower_id} -> {self.user_id}"
