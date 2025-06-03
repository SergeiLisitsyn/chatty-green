# ads/forms.py

from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'link', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control comment-input',
                'style': 'height: 50px;',
                'placeholder': 'Введите заголовок объявления'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control comment-input',
                'style': 'height: 120px;',
                'placeholder': 'Введите описание объявления'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control comment-input',
                'placeholder': 'Введите ссылку'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control comment-input'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control comment-input'
            }),
        }
