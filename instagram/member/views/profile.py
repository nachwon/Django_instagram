from django.shortcuts import render

from member.models import User

__all__ = (
    'user_profile',
)


def user_profile(request, pk):
    all_users = User.objects.all().exclude(pk=request.user.pk)
    user = User.objects.get(pk=pk)
    context = {
        'profile_user': user,
        'all_users': all_users,
    }
    return render(request, 'member/profile.html', context)

