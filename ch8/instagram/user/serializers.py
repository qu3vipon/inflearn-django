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
            password=validated_data["password"],
        )
        return user


class UserMeResponseSerializer(serializers.ModelSerializer):
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


class UserFollowResponseSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    follower_id = serializers.PrimaryKeyRelatedField(source="follower", read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "user_id", "follower_id", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()
    followers_count = serializers.IntegerField()
    followings_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "posts_count", "followers_count", "followings_count"]
