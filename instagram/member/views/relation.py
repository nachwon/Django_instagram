from django.shortcuts import redirect

from member.models import User, Relationship

__all__ = (
    'follow_toggle',
)


def follow_toggle(request, pk):
    relation = Relationship.objects.filter(from_user=request.user, to_user=User.objects.get(pk=pk))
    if relation.exists():
        relation.delete()
    else:
        Relationship.objects.create(from_user=request.user,
                                    to_user=User.objects.get(pk=pk))
    url = request.META['HTTP_REFERER']
    return redirect(url)
