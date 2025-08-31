from django.contrib import admin
from .models import Post, Like, Comment, Category, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_name", "profile_picture")  # Show in list view
    search_fields = ("user__username", "profile_name")
    fields = ("user", "profile_name", "profile_picture", "about", "cover_photo")  # Order inside form
    
    
# Post Admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'author__username')
    list_filter = ('created_at', 'author')

    def get_profile_name(self, obj):
        return obj.author.profile.profile_name if hasattr(obj.author, 'profile') else ''
    get_profile_name.short_description = 'Profile Name'
    
    
# Register Models
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile, ProfileAdmin)