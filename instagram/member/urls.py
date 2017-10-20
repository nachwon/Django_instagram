from django.conf.urls import url

from member.views import signup, user_login, user_logout, user_profile

urlpatterns = [
    url(r'signup/$', signup, name='signup'),
    url(r'login/$', user_login, name='login'),
    url(r'logout/$', user_logout, name='logout'),
    url(r'profile/$', user_profile, name='user_profile'),
]