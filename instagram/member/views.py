from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.forms import SignUpForm, LoginForm
from post.views import post_list


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            username = form['username']
            email = form['mail']
            password = form['password_2']
            User.objects.create_user(username=username, email=email, password=password)
            signed_up = True

        else:
            signed_up = False
            context = {
                'signed_up': signed_up,
                'form': form
            }
            return render(request, 'member/signup.html', context)
    else:
        signed_up = False
        form = SignUpForm()

    context = {
        'signed_up': signed_up,
        'form': form
    }

    return render(request, 'member/signup.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect(post_list)
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'member/login.html', context)


def user_logout(request):
    logout(request)
    return redirect(post_list)
