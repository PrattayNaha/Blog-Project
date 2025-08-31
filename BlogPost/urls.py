from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import include

urlpatterns = [
    path('', views.index, name= 'index'),
    path('post/<str:pk>', views.post, name = 'post'),

    path('blog_create', views.blog_create, name='blog_create'),
    path('blog_edit/<str:pk>', views.blog_edit, name='blog_edit'),
    path('blog_delete/<str:pk>', views.blog_delete, name='blog_delete'),
    path('login/', views.custom_login, name='custom_login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='custom_login'), name='logout'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('comment/<str:pk>/', views.add_comment, name='add_comment'),
    path('feed/', views.index, name='blog_feed'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    
    path("change-profile-pic/", views.change_profile_pic, name="change_profile_pic"),
    path("change-cover-photo/", views.change_cover_photo, name="change_cover_photo"),
    path("edit-about/", views.edit_about, name="edit_about"),

    path("profile/<str:username>/", views.profile_view, name="profile"),
    
    path("search/", views.search, name='search')
]
    