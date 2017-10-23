from urllib.parse import urlparse

from django.shortcuts import redirect
from django.urls import reverse


def login_required(func):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            base_url = reverse('member:login')
            referer = urlparse(request.META['HTTP_REFERER']).path
            url = f'{base_url}?next={referer}'
            return redirect(url)
        return func(*args, **kwargs)
    return decorator
