# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        ), 
        help_text=None  # supprime le texte d'aide
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Bio',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'photo']