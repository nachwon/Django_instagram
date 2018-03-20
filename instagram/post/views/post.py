# from django.contrib.auth.decorators import login_required
from itertools import chain

from django.core.exceptions import PermissionDenied
from member.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from member.models import User
from ..models import Post, PostLike
from ..forms import PostAddForm

__all__ = (
    'post_list',
    'post_detail',
    'post_add',
    'post_delete',
    'post_like',
)


def post_list(request):
    if request.user.is_authenticated:
        all_users = User.objects.all().exclude(pk=request.user.pk)
        user = request.user
        user_posts = user.post_set.all()
        following_users = user.following.all()
        for following_user in following_users:
            following_posts = following_user.post_set.all()
            user_posts = chain(user_posts, following_posts)

        result_list = sorted(user_posts, key=lambda instance: instance.created_date)
        posts = list(result_list)[::-1]
        liked = user.postlike_set.all()
        like_list = [i.post_id for i in liked]
    else:
        posts = None
        user = request.user
        like_list = None
        all_users = None

    context = {
        'posts': posts,
        'liked': like_list,
        'user': user,
        'all_users': all_users
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, pk):
    if request.user.is_authenticated:
        all_users = User.objects.all().exclude(pk=request.user.pk)
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        liked = user.postlike_set.all()
        liked_list = [i.post_id for i in liked]
    else:
        all_users = None
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        liked_list = None
    context = {
        'post': post,
        'user': user,
        'liked': liked_list,
        'all_users': all_users,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_like(request, pk):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        if PostLike.objects.filter(author_id=user.pk, post_id=post.pk).exists():
            liked = PostLike.objects.get(author_id=user.pk, post_id=post.pk)
            liked.delete()
        else:
            PostLike.objects.create(author_id=user.pk, post_id=post.pk)

    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostAddForm()
    all_users = User.objects.all().exclude(pk=request.user.pk)
    context = {
        'form': form,
        'all_users': all_users,
    }
    return render(request, 'post/post_add.html', context)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('post:post_list')
    raise PermissionDenied('잘못된 접근입니다.')


