from django import forms
from post.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "author_name"]
        labels = {
            "title": "제목",
            "body": "본문",
            "author_name": "작성자",
        }
