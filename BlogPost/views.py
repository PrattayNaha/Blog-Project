from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Like, Comment, Category, Profile
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count, Q

   
def index(request):
    posts = Post.objects.all().order_by("-created_at")
    categories = Category.objects.all()
    
    popular_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj, "categories": categories, "popular_posts": popular_posts})

# @login_required
# def blog_feed(request):
#     posts = Post.objects.all().order_by("-created_at")
#     categories = Category.objects.all()

#     popular_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

#     paginator = Paginator(posts, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "index.html", {"page_obj": page_obj, "categories": categories, "popular_posts": popular_posts})

def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'posts.html', {'posts': posts})

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='custom_login')
def blog_list(request):
    blogs = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'blogs': blogs})

@login_required(login_url='custom_login')
def blog_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('profile', username=request.user.username)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_name = request.POST['profile_name']

        if password != confirm_password:
            messages.info(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        Profile.objects.create(user=user, profile_name=profile_name)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile', username=request.user.username)

    return render(request, 'signup.html')

@login_required(login_url='custom_login')
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post', pk=pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            Comment.objects.create(post=post, author=request.user, body=body)
    return redirect('post', pk=post.pk)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
    return redirect('post', pk=comment.post.id)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all()
    categories = Category.objects.all()
    
    popular_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:3]
    
    paginator = Paginator(posts, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page_obj': page_obj, 
        'selected_category': category, 
        'categories': categories, 
        'popular_posts': popular_posts,
    })

@login_required
def change_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
    return redirect('profile', username=request.user.username)

@login_required
def change_cover_photo(request):
    if request.method == 'POST' and request.FILES.get('cover_photo'):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.cover_photo = request.FILES['cover_photo']
        profile.save()
    return redirect('profile', username=request.user.username)

@login_required
def edit_about(request):
    if request.method == 'POST':
        about_text = request.POST.get('about')
        request.user.profile.about = about_text
        request.user.profile.save()
        return redirect("profile", username=request.user.username)
    


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    blogs = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, "profile.html", {
        "profile": profile,
        "user_obj": user,
        "blogs": blogs
    })

def search(request):
    query = request.GET.get('query')
    search_by = request.GET.get('search_by')
    
    if not query:
        posts = Post.objects.none()
    else:
        if search_by == 'author':
            posts = Post.objects.filter(
                Q(author__username__icontains=query) |
                Q(author__profile__profile_name__icontains=query)
            )
        else:
            posts = Post.objects.filter(title__icontains=query)
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    popular_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:3]

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'popular_posts': popular_posts,
        'search_query': query,
        'search_by': search_by,
    })
