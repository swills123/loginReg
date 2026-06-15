from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Comment, Like, Follow, Notification


@login_required(login_url='login')
def board_view(request):
    unread_count = request.user.notifications.filter(is_read=False).count()
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(author=request.user, content=content)
            messages.success(request, 'Post added!')
        return redirect('board')

    posts = Post.objects.all().order_by('-created_at')

    # the set of users I currently follow (one query)
    following_ids = set(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )

    # attach like + follow info to each post
    for post in posts:
        post.like_count = post.likes.count()
        post.user_liked = post.likes.filter(user=request.user).exists()
        post.is_following_author = post.author_id in following_ids

    my_following_count = request.user.following.count()
    my_follower_count = request.user.followers.count()

    return render(request, 'board.html', {
        'posts': posts,
        'my_following_count': my_following_count,
        'my_follower_count': my_follower_count,
        'unread_count': unread_count,
    })


@login_required(login_url='login')
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('board')


@login_required(login_url='login')
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('board')


@login_required(login_url='login')
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('board')


@login_required(login_url='login')
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # already liked so unlike it
    else:
        # notify the post author (not for liking your own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                action='liked your post',
                post=post,
            )
    # return to whichever page the like came from (home or board)
    next_url = request.POST.get('next', 'board')
    return redirect(next_url)


@login_required(login_url='login')
def toggle_follow_view(request, user_id):
    target = get_object_or_404(User, id=user_id)

    # you can't follow yourself
    if target == request.user:
        return redirect('board')

    follow, created = Follow.objects.get_or_create(
        follower=request.user,   # me
        following=target         # the person I clicked follow on
    )
    if not created:
        follow.delete()  # already following so unfollow
    else:
        # notify the person who just got followed
        Notification.objects.create(
            recipient=target,
            sender=request.user,
            action='started following you',
        )
    next_url = request.POST.get('next', 'board')
    return redirect(next_url)


@login_required(login_url='login')
def follow_list_view(request, user_id):
    target = get_object_or_404(User, id=user_id)
    following = target.following.all()    # who they follow
    followers = target.followers.all()    # who follows them
    return render(request, 'follower_list.html', {
        'target': target,
        'following': following,
        'followers': followers,
    })


@login_required(login_url='login')
def notifications_view(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required(login_url='login')
def mark_read_view(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')


@login_required(login_url='login')
def mark_all_read_view(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notifications')

@login_required(login_url='login')
def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all().order_by('-created_at')

    # attach like info so the like button shows count + highlight
    for post in posts:
        post.like_count = post.likes.count()
        post.user_liked = post.likes.filter(user=request.user).exists()

    is_following = Follow.objects.filter(follower=request.user, following=user).exists() if request.user != user else False

    return render(request, 'profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
    })
