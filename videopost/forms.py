# videopost/forms.py

from django import forms
from .models import VideoPost, VideoComment


class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title', 'description', 'video_url', 'video_file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок видео'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Описание видео'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL видео'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Заголовок должен содержать минимум 5 символов.')
        return title


class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment  # эта модель должна быть в твоих моделях
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'placeholder': 'Напишите комментарий...'})
