from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import CustomUser, Follow


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],  # 비밀번호 해싱
        )
        return user


class UserMeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserMeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

    def update(self, instance, validated_data):
        if password := validated_data.get("password"):
            validated_data["password"] = make_password(password)
        return super().update(instance, validated_data)


class UserFollowReadSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    follower_id = serializers.PrimaryKeyRelatedField(source="follower", read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "user_id", "follower_id", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()
    followers_count = serializers.IntegerField()
    followings_count = serializers.IntegerField()

    # posts_count = serializers.SerializerMethodField()
    # followers_count = serializers.SerializerMethodField()
    # followings_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "posts_count", "followers_count", "followings_count"]

    # def get_posts_count(self, obj):
    #     return obj.posts.count()
    #
    # def get_followers_count(self, obj):
    #     return obj.followers.count()
    #
    # def get_followings_count(self, obj):
    #     return obj.followings.count()
