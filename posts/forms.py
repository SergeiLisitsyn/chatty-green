# posts/forms.py
from django import forms
from .models import Post

from .models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок поста'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Текст поста'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Заголовок должен содержать минимум 5 символов.')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Комментарий состоит только из текста

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'placeholder': 'Write a comment...'})