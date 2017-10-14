from django.shortcuts import render, redirect

from config.settings import MEDIA_ROOT
from post.models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_add(request):
    if request.method == 'GET':
        return render(request, 'post/post_add.html')

    if request.method == 'POST':
        photo=request.FILES['post-photo']

        Post.objects.create(photo=photo)

        return redirect(post_list)



def comment_add(request, pk):
    post = Post.objects.get(pk=pk)
    PostComment.objects.create(post=post, content=request.POST['comment'])
    return redirect(post_list)