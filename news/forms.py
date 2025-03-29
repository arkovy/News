from django import forms

from .models import Comment, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'excerpt', 'content', 'image_name', 'tags']
        labels = {
            'title': 'Заголовок',
            'excerpt': 'Краткое содержание',
            'content': 'Содержимое',
            'image_name': 'Изображение',
            'tags': 'Теги',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['news']
        labels = {
            'user_name': 'Your Name',
            'user_email': 'Your Email',
            'text': 'Your Comment'
        }
