# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import ForumPost
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Reply


class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30, 
        required=False, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Prénom',
            }
        ), 
        help_text=None
    )

    last_name = forms.CharField(
        max_length=30, 
        required=False, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom',
            }
        ), 
        help_text=None
    )

    gender = forms.ChoiceField(
            required=True, 
            choices=UserProfile.GENDER_CHOICES,
            widget=forms.RadioSelect()
        )
    
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Pseudo*',
            }
        ), 
        help_text=None  # supprime le texte d'aide
    )
    
    email = forms.EmailField(   
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Adresse email*',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe*',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirmation mot de passe*',
            }
        ),
        help_text=None  # supprime le texte d'aide
    )
    
    bio = forms.CharField(
        label = "Description bio",
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
        label = "Photo",
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
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'photo']

class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 50%;',
            'placeholder': 'Titre'  
        })
    )
    
    content = forms.CharField(
        widget=CKEditorUploadingWidget()
    )
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

class ReplyModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        required=True
    )

    class Meta:
        model = Reply
        fields = ['content']