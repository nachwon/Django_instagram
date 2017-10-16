from django.conf.urls import url

from member.views import signup, user_login, logging, user_logout

urlpatterns = [
    url(r'signup/$', signup, name='signup'),
    url(r'login/$', user_login, name='login'),
    url(r'loggin-in/$', logging, name='logging'),
    url(r'logout/$', user_logout, name='logout'),
]