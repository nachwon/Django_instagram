import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, PostComment
from .forms import PostAddForm


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    context = {
        'posts': posts,
        'user': user,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_like(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    post.liked.add(user)
    post.save()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def post_dislike(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    post.liked.remove(user)
    post.save()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            photo = form.cleaned_data['photo']
            content = form.cleaned_data['content']
            Post.objects.create(author=user, photo=photo, content=content)
            return redirect(post_list)

    elif request.method == 'GET':
        form = PostAddForm()
    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    os.remove(f'media/{post.photo.name}')
    return redirect(post_list)


@login_required
def comment_add(request, pk):
    if request.user.is_authenticated:
        user = request.user
    post = Post.objects.get(pk=pk)
    PostComment.objects.create(author=user, post=post, content=request.POST['comment'])
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


@login_required
def comment_delete(request, pk, comment_pk):
    comment = PostComment.objects.filter(pk=comment_pk)
    comment.delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')

