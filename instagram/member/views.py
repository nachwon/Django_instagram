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
            password_1 = form['password_1']
            password_2 = form['password_2']
            if password_1 == password_2 and not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password_1)
                context = {
                    'signed_up': True,
                }
            elif User.objects.filter(username=username).exists():
                form = SignUpForm(request.POST)
                context = {
                    'form': form,
                    'no_match': '이미 유저가 있습니다.',
                }
            elif password_1 != password_2:
                form = SignUpForm(request.POST)
                context = {
                    'form': form,
                    'no_match': '비밀번호가 일치하지 않습니다.',
                }
    else:
        form = SignUpForm()
        context = {
            'form': form
        }
    return render(request, 'member/signup.html', context)


def user_login(request):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'member/login.html', context)


def logging(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(post_list)
    else:
        return redirect(user_login)


def user_logout(request):
    logout(request)
    return redirect(post_list)
