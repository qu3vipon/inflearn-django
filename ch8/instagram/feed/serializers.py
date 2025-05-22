from rest_framework import serializers

from feed.models import Post, PostComment, PostLike
from user.models import CustomUser


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user_id", "image", "description", "created_at"]


class PostCommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(source="post", queryset=Post.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent", queryset=PostComment.objects.all(), required=False,
    )

    class Meta:
        model = PostComment
        fields = ["id", "post_id", "user_id", "parent_id", "content", "created_at"]

    def validate(self, attrs):
        post, parent = attrs.get("post"), attrs.get("parent")

        # 대댓글 작성하려는 경우
        if parent:
            if parent.post != post:
                raise serializers.ValidationError("댓글의 게시글과 대댓글의 게시글이 일치하지 않습니다.")
            if parent.parent is not None:
                raise serializers.ValidationError("대댓글에는 다시 대댓글을 작성할 수 없습니다.")
        return attrs


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]

class PostCommentSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ["id", "user", "parent_id", "content", "replies", "created_at"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return PostCommentSerializer(obj.replies.all(), many=True).data
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer()
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "user", "image", "description", "comments", "created_at"]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["id", "post_id", "user_id", "created_at"]
