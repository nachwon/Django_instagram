import os

from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, PostComment
from .forms import PostAddForm


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


def post_add(request):
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            content = form.cleaned_data['content']
            Post.objects.create(photo=photo, content=content)
            return redirect(post_list)

    elif request.method == 'GET':
        form = PostAddForm()
    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    os.remove(f'media/{post.photo.name}')
    return redirect(post_list)


def comment_add(request, pk):
    post = Post.objects.get(pk=pk)
    PostComment.objects.create(post=post, content=request.POST['comment'])
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')


def comment_delete(request, pk, comment_pk):
    comment = PostComment.objects.filter(pk=comment_pk)
    comment.delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post-{pk}')

