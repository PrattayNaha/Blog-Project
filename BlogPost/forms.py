from django import forms
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category']
        widgets= {
            'body': CKEditor5Widget(),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_name = forms.CharField(max_length=100, required=True, help_text='Enter your profile name.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "profile_name")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        profile_name = self.cleaned_data.get("profile_name")
        if commit:
            user.save()
            profile_name = self.cleaned_data.get("profile_name")
            Profile.objects.update_or_create(
                user=user,
                defaults={"profile_name": profile_name}
            )

        return user