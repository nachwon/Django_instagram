from django.contrib.auth import logout
from django.shortcuts import render, redirect
from member.forms import SignUpForm, LoginForm
from post.views import post_list


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.signup()
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect(post_list)
    else:
        form = LoginForm()
    context = {
        'login_form': form
    }
    return render(request, 'member/login.html', context)


def user_logout(request):
    logout(request)
    return redirect(post_list)
