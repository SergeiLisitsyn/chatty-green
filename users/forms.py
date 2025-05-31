# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'width: 100%; height: 80px; resize: none;',
            'placeholder': 'Напишите о себе...'
        }),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'contacts', 'password1', 'password2']


class CustomUserEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'contacts']
        widgets = {
                    'avatar': forms.ClearableFileInput(attrs={'id': 'id_avatar'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
