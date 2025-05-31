#users/forms.py

from django import forms
from django.contrib.admin import display
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # добавляем класс для Bootstrap
            'style': 'width: 100%; height: 80px; resize: none;',  # задаем размеры для поля
            'placeholder': 'Напишите о себе...'  # добавляем подсказку
        }),
        required=False
    )
    # Добавляем поле для выбора отображения email
    display_email = forms.BooleanField(
        required=False,
        label="Показывать мой email в профиле"
    )


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'contacts', 'password1', 'password2', "display_email"]


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'avatar', 'bio', 'contacts', "display_email"]


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
