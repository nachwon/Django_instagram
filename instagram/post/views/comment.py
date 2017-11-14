from member.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Post, PostComment

__all__ = (
    'comment_add',
    'comment_delete',
)


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
