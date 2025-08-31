from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = CKEditor5Field('body', config_name="default")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="posts")
    
    def __str__(self):
        return self.title
    
    
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user} likes {self.post}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile', default='default-profile.jpg')
    about = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='images/cover', default='default-cover.jpg')

    def __str__(self):
        return self.profile_name or self.user.username

