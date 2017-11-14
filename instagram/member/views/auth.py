from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render, redirect


from member.forms import SignUpForm, LoginForm

__all__ = (
    'signup',
    'user_login',
    'user_logout',
)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            signed_up = True

        else:
            signed_up = False

    else:
        signed_up = False
        form = SignUpForm()

    context = {
        'signed_up': signed_up,
        'signup_form': form
    }

    return render(request, 'member/signup.html', context)


def user_login(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            if next_url:
                return redirect(next_url)
            return redirect('post:post_list')
    else:
        form = LoginForm()
    context = {
        'login_form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'scope_fields': settings.FACEBOOK_SCOPE['scope'],
    }
    return render(request, 'member/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('post:post_list')
