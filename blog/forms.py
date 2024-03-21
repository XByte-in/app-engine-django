from django.forms import ModelForm
from .models import Post, Comment

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
