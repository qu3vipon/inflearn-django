from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = "email"  # 사용자의 인증에 사용할 필드를 지정하는 속성
    REQUIRED_FIELDS = ["username"]  # createsuperuser 명령을 실행할 때 필수로 입력해야 하는 추가 필드를 지정하는 속성


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)  # 팔로우 당하는 사용자
    follower = models.ForeignKey(CustomUser, related_name="followings", on_delete=models.CASCADE)  # 팔로우 하는 사용자
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "follower")  # 동일한 관계 중복 방지
        ordering = ["-created_at"]  # 최신 순 정렬

    def __str__(self):
        return f"{self.follower_id} -> {self.user_id}"
