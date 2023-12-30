from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Импорт вашей пользовательской модели
from django import forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
                                attrs={"class": "focus:outline-none",
                                       'placeholder': 'mail@mail.com',
                                       }))
    username = forms.CharField(required=True, widget=forms.TextInput(
                                attrs={"class": "focus:outline-none",
                                       'placeholder': 'Enter username...',
                                       }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
                                attrs={"class": "focus:outline-none",
                                       'placeholder': 'Enter password',
                                       }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
                                attrs={"class": "focus:outline-none",
                                       'placeholder': 'Enter same password',
                                       }))
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser  # Используйте вашу модель CustomUser вместо User
        fields = ("username", "email", "password1", "password2", "is_seller")
