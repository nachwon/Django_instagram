from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from member.forms import SignUpForm, LoginForm
from post.views import post_list


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
        'facebook_app_id': settings.FACEBOOK_APP_ID
    }
    return render(request, 'member/login.html', context)


def facebook_login(request):
    url_access_token = "https://graph.facebook.com/v2.10/oauth/access_token"
    redirect_uri = '{scheme}://{host}{relative_url}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        relative_url=reverse('member:facebook_login'),
    )
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': redirect_uri,
        'client_secret': settings.FACEBOOK_SECRET_CODE,
        'code': request.GET.get('code'),
    }
    response = requests.get(url_access_token, params=params)
    result = response.json()
    pprint(result)

    return HttpResponse(result)


def user_logout(request):
    logout(request)
    return redirect('post:post_list')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'member/profile.html')
