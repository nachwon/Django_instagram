import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, PostComment, PostLike, SubRelation
from .forms import PostAddForm


def post_list(request):
    # posts = Post.objects.all().order_by('-created_date')
    if request.user.is_authenticated:
        user = request.user
        relations = SubRelation.objects.filter(follower=user)
        if not relations:
            posts = None
        else:
            for relation in relations:
                posts = (
                    relations[0].following.post_set.all()
                    | relation.following.post_set.all()
                )
            posts = (posts | Post.objects.filter(author=user))
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
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        user = request.user
        liked = user.postlike_set.all()
        liked_list = [i.post_id for i in liked]
    else:
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

