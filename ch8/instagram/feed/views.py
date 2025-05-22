from django.db.models import Prefetch
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, \
    DestroyAPIView, GenericAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from feed.models import Post, PostComment, PostLike
from feed.serializers import PostSerializer, PostCommentCreateSerializer, PostDetailSerializer, PostLikeSerializer


class PostCursorPagination(CursorPagination):
    page_size = 1
    ordering = "-created_at"


class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = PostCursorPagination

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class PostCommentView(CreateAPIView):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        request.data["post_id"] = self.kwargs.get("post_id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class PostDetailView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_url_kwarg = "post_id"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return super().get_queryset().select_related("user").prefetch_related(
            Prefetch(
                "comments",
                queryset=PostComment.objects.filter(parent=None).prefetch_related("replies", "user")
            )
        )

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("게시물을 삭제할 권한이 없습니다.")

        instance.delete()

class PostCommentDestroyView(DestroyAPIView):
    queryset = PostComment.objects.all()
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("댓글을 삭제할 권한이 없습니다.")

        # 1) 댓글 삭제 -> 대댓글(CASCADE) => Hard Delete
        instance.delete()

        # 2) 댓글 삭제 -> 대댓글 유지 => Soft Delete
        # if instance.parent is None and instance.replies.exists():
        #     instance.content = "삭제된 댓글입니다."
        #     instance.save()
        # else:
        #     instance.delete()


class PostLikeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id):
        like, created = PostLike.objects.get_or_create(post_id=post_id, user_id=request.user.id)
        serializer = PostLikeSerializer(like)
        if created:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        PostLike.objects.filter(post_id=post_id, user_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
