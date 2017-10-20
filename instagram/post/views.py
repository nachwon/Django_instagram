import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, PostComment, PostLike
from .forms import PostAddForm


def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        liked = user.postlike_set.all()
        like_list = [i.post_id for i in liked]
    else:
        posts = None
        user = None
        like_list = None

    context = {
        'posts': posts,
        'liked': like_list,
        'user': user,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        liked = user.postlike_set.all()
        liked_list = [i.post_id for i in liked]
    else:
        post = None,
        user = None,
        liked_list = None
    context = {
        'post': post,
        'user': user,
        'liked': liked_list,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_like(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    PostLike.objects.create(author_id=user.pk, post_id=post.pk)
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def post_dislike(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    liked = PostLike.objects.get(author_id=user.pk, post_id=post.pk)
    liked.delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def post_add(request):
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostAddForm()
    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('post:post_list')
    raise PermissionDenied('잘못된 접근입니다.')


@login_required
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    PostComment.objects.create(author=user, post=post, content=request.POST['comment'])
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def comment_delete(request, pk, comment_pk):
    comment = PostComment.objects.filter(pk=comment_pk)
    comment.delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')

