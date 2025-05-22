from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.views import View

from post.models import Post
from post.forms import PostForm


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {"posts": posts}
        return render(
            request, "post_list.html", context
        )

class PostCreateView(View):
    def get(self, request):
        context = {"form": PostForm}
        return render(
            request, "post_create.html", context
        )

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            author_name = form.cleaned_data["author_name"]

            post = Post.objects.create(
                title=title, body=body, author_name=author_name
            )
            context = {"post": post}
            return render(
                request, "post_detail.html", context
            )
        return redirect("posts")


class PostDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        context = {"post": post}
        return render(
            request, "post_detail.html", context
        )

class PostLikeView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.points = F("points") + 1
        post.save()
        post.refresh_from_db()
        return render(
            request, "post_detail.html", {"post": post}
        )
