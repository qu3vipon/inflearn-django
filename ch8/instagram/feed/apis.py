from django.db.models import Prefetch
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404, \
    DestroyAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from feed.models import Post, PostComment, PostLike
from feed.serializers import PostSerializer, PostDetailSerializer, PostCommentCreateSerializer, PostLikeSerializer


class PostCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


class PostsAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class PostDetailAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'comments',
                queryset=PostComment.objects.filter(parent=None).prefetch_related('replies'),
            )
        )

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("게시물을 삭제할 권한이 없습니다.")

        instance.delete()

class PostCommentCreateAPIView(CreateAPIView):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        request.data["post_id"] = self.kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class PostCommentDestroyAPIView(DestroyAPIView):
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("댓글을 삭제할 권한이 없습니다.")

        instance.delete()


class PostLikeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        like, _ = PostLike.objects.get_or_create(post_id=kwargs["pk"], user_id=request.user.id)
        serializer = PostLikeSerializer(like)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        PostLike.objects.filter(post_id=kwargs["pk"], user_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
