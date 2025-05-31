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
                'placeholder': 'Заголовок поста',
                'style': '''
                    font-family: "Tilda Sans", sans-serif;
                    font-size: 16px;
                    background-color: #ffffff;  # Белый фон
                    border: 1px solid #ced4da;  # Серая рамка
                    border-radius: 4px;         # Закругленные углы
                    padding: 8px 12px;         # Отступы внутри поля
                '''
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Текст поста',
                'style': '''
                    font-family: "Tilda Sans", sans-serif;
                    font-size: 14px;
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    padding: 12px;
                '''
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