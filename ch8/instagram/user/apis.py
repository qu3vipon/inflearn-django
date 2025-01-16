from django.db import IntegrityError
from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, GenericAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import CustomUser, Follow
from user.serializers import UserSignUpSerializer, UserMeReadSerializer, UserMeUpdateSerializer, UserFollowReadSerializer, \
    UserProfileSerializer


class UserSignUpAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignUpSerializer


class UserMeAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]  # 인증된 유저만 호출 가능하도록 설정
    authentication_classes = [JWTAuthentication]  # 인증 방식은 JWT로 설정

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserMeReadSerializer
        elif self.request.method == "PATCH":
            return UserMeUpdateSerializer
        return super().get_serializer_class()


class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = "user_id"
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # 객체를 가져올 때 count를 미리 가져오기
        user = self.queryset.prefetch_related("posts", "followers", "followings").annotate(
            posts_count=Count("posts"),
            followers_count=Count("followers"),
            followings_count=Count("followings")
        ).get(id=self.kwargs["pk"])
        return user


class UserFollowAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        if user_id == request.user.id:
            raise PermissionDenied("자기 자신을 팔로잉 할 수 없습니다.")

        follow, _ = Follow.objects.get_or_create(user_id=user_id, follower_id=request.user.id)
        serializer = UserFollowReadSerializer(follow)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        Follow.objects.filter(user_id=user_id, follower_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
