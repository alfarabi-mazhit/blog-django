from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # поле для выбора категорий
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'published_date', 'image', 'categories']  # поля для заполнения

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
