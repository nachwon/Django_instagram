from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import logout, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from member.forms import SignUpForm, LoginForm
from member.models import User, Relationship


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


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        type: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        user_id: int

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data['email']
            self.url_picture = data['picture']['data']['url']

    url_access_token = "https://graph.facebook.com/v2.10/oauth/access_token"
    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_SECRET_CODE
    redirect_uri = '{scheme}://{host}{relative_url}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        relative_url=reverse('member:facebook_login'),
    )
    code = request.GET.get('code')

    def get_access_token_info(code_input):
        params = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code_input,
        }

        response = requests.get(url_access_token, params=params)

        return AccessTokenInfo(**response.json())

    def get_debug_token_info(access_token_input):

        app_access_token = f'{app_id}|{app_secret_code}'

        verify_url = 'https://graph.facebook.com/debug_token'
        verify_params = {
            'input_token': access_token_input,
            'access_token': app_access_token,
        }

        verification = requests.get(verify_url, verify_params)
        return DebugTokenInfo(**verification.json()['data'])

    access_token = get_access_token_info(code).access_token
    debug_token_info = get_debug_token_info(access_token)

    url_graph_user_info = 'https://graph.facebook.com/me'
    user_info_fields = [
        'id',
        'name',
        'picture',
        'email'
    ]
    graph_user_params = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, graph_user_params)
    result = response.json()
    user_info = UserInfo(data=result)

    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
        )

    login(request, user)

    return redirect('post:post_list')


class FrontFacebookLogin(View):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    def get(self, request):
        app_id = settings.FACEBOOK_APP_ID
        app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
        app_access_token = f'{app_id}|{app_secret_code}'
        code = request.GET.get('code')

        def get_access_token_info(code_value):
            # 사용자가 페이스북에 로그인하기 위한 링크에 있던 'redirect_uri' GET파라미터의 값과 동일한 값
            redirect_uri = '{scheme}://{host}{redirect_url}'.format(
                scheme=request.scheme,
                host=request.META['HTTP_HOST'],
                redirect_url=reverse('member:front-facebook-login'),
            )
            print('redirect_uri:', redirect_uri)
            # 액세스 토큰을 요청하기 위한 엔드포인트
            url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
            # 액세스 토큰 요청의 GET파라미터 목록
            params_access_token = {
                'client_id': app_id,
                'redirect_uri': redirect_uri,
                'client_secret': app_secret_code,
                'code': code_value,
            }
            # 요청 후 결과를 받아옴
            response = requests.get(url_access_token, params_access_token)
            # 결과는 JSON형식의 텍스트이므로 아래와 같이 사용
            # json.loads(response.content) 와 같음

            # AccessTokenInfo(access_token=response.json()['access_token'],
            #    'token_type'=response.json()['token_type.....
            return self.AccessTokenInfo(**response.json())

        def get_debug_token_info(token):
            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return self.DebugTokenInfo(**response.json()['data'])

        # 전달받은 code값으로 AccessTokenInfo namedtuple을 반환
        access_token_info = get_access_token_info(code)
        # namedtuple에서 'access_token'속성의 값을 가져옴
        access_token = access_token_info.access_token
        # DebugTokenInfo 가져오기
        debug_token_info = get_debug_token_info(access_token)

        # 유저정보 가져오기
        user_info_fields = [
            'id',
            'name',
            'picture',
            'email',
        ]
        url_graph_user_info = 'https://graph.facebook.com/me'
        params_graph_user_info = {
            'fields': ','.join(user_info_fields),
            'access_token': access_token,
        }
        response = requests.get(url_graph_user_info, params_graph_user_info)
        result = response.json()
        user_info = self.UserInfo(data=result)

        data = {
            'facebook_user_id': user_info.id,
            'access_token': access_token,
        }
        return JsonResponse(data)


def user_logout(request):
    logout(request)
    return redirect('post:post_list')


def user_profile(request, pk):
    all_users = User.objects.all().exclude(pk=request.user.pk)
    user = User.objects.get(pk=pk)
    context = {
        'profile_user': user,
        'all_users': all_users,
    }
    return render(request, 'member/profile.html', context)


def follow_toggle(request, pk):
    relation = Relationship.objects.filter(from_user=request.user, to_user=User.objects.get(pk=pk))
    if relation.exists():
        relation.delete()
    else:
        Relationship.objects.create(from_user=request.user,
                                    to_user=User.objects.get(pk=pk))
    url = request.META['HTTP_REFERER']
    return redirect(url)
