from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import CustomUser, Follow
from user.serializers import UserSignUpSerializer, UserMeResponseSerializer, UserMeUpdateSerializer, \
    UserFollowResponseSerializer, UserProfileSerializer


class UserSignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignUpSerializer


class UserMeView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserMeResponseSerializer
    permission_classes = [IsAuthenticated]  # 인증된 유저만 호출
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserMeResponseSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UserMeUpdateSerializer
        return super().get_serializer_class()


class UserFollowView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        if user_id == request.user.id:
            raise PermissionDenied("자기 자신을 팔로우 할 수 없습니다.")

        follow, created = Follow.objects.get_or_create(
            user_id=user_id, follower_id=request.user.id
        )
        serializer = UserFollowResponseSerializer(follow)

        if created:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        # 조건에 맞는 팔로우 관계가 존재하는 경우, 데이터 삭제. 그렇지 않으면 아무 일도 발생하지 않음
        Follow.objects.filter(user_id=user_id, follower_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = "user_id"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            "posts", "followers", "followings"
        ).annotate(
            posts_count=Count("posts", distinct=True),
            followers_count=Count("followers", distinct=True),
            followings_count=Count("followings", distinct=True),
        )
