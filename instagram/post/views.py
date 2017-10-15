import os

from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from post.models import Post, PostComment


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method == 'GET':
        return render(request, 'post/post_add.html')

    if request.method == 'POST':
        try:
            photo = request.FILES['post-photo']
        except MultiValueDictKeyError:
            context = {
                'error': '사진을 올려주세요!'
            }
            return render(request, 'post/post_add.html', context)
        content = request.POST['content']
        Post.objects.create(photo=photo, content=content)
        return redirect(post_list)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    os.remove(f'media/{post.photo.name}')
    return redirect(post_list)


def comment_add(request, pk):
    post = Post.objects.get(pk=pk)
    PostComment.objects.create(post=post, content=request.POST['comment'])
    return redirect(f'/post/#post-{pk}')


def comment_delete(request, pk, comment_pk):
    comment = PostComment.objects.filter(pk=comment_pk)
    comment.delete()
    return redirect(f'/post/#post-{pk}')

