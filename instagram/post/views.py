from django.shortcuts import render, redirect

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
        photo = request.FILES['post-photo']
        content = request.POST['content']
        Post.objects.create(photo=photo, content=content)

        return redirect(post_list)


def post_delete(request):
    pass


def comment_add(request, pk):
    post = Post.objects.get(pk=pk)
    PostComment.objects.create(post=post, content=request.POST['comment'])
    return redirect(post_list)


def comment_delete(request, pk, comment_pk):
    comment = PostComment.objects.filter(pk=comment_pk)
    comment.delete()
    return redirect(post_list)

