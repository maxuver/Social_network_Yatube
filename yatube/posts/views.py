from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from .utils import get_page_context

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post

User = get_user_model()

WORDS_LIMIT_IN_CAPTION = 30


@cache_page(20)
def index(request):
    post_list = Post.objects.all()
    template = 'posts/index.html'
    context = {
        'page_obj': get_page_context(post_list, request),
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': get_page_context(post_list, request),
    }
    return render(request, template, context)


def profile(request, username):
    following = request.user.is_authenticated
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    template = 'posts/profile.html'
    if following:
        following = author.following.filter(
            user=request.user).exists()
    template = 'posts/profile.html'
    context = {
        'page_obj': get_page_context(post_list, request),
        'author': author,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    title = f'Пост {post.text[:WORDS_LIMIT_IN_CAPTION]}'
    context = {
        'form': form,
        'post': post,
        'title': title
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    template = 'posts/create_post.html'
    context = {'form': form}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    template = 'posts/create_post.html'
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, template, context)


@login_required
def follow_index(request):
    posts = Post.objects.filter(
        author__following__user=request.user
    ).select_related('author', 'group')
    page_obj: get_page_context(posts, request)
    return render(request, 'posts/follow.html',
                  {'page_obj': get_page_context(posts, request)})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    user_follower = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    )
    user_follower.delete()
    return redirect('posts:profile', username)
