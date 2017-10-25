from django.conf.urls import url

from member.views import signup, user_login, user_logout, user_profile, facebook_login, follow_toggle

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^facebook-login/$', facebook_login, name='facebook_login'),
    url(r'^profile/(?P<pk>\d+)/$', user_profile, name='user_profile'),
    url(r'^follow/(?P<pk>\d+)/$', follow_toggle, name='follow_toggle'),
]