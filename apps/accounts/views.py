from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from messageboard.models import Post, Follow


def home_view(request):
    context = {}
    if request.user.is_authenticated:
        # show recent posts from people I follow
        following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        posts = Post.objects.filter(author_id__in=following_ids).order_by('-created_at')[:20]

        # attach like info so the like button shows count + highlight
        for post in posts:
            post.like_count = post.likes.count()
            post.user_liked = post.likes.filter(user=request.user).exists()

        context['posts'] = posts
    return render(request, 'home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')