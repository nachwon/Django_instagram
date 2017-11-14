from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<pk>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^follow/(?P<pk>\d+)/$', views.follow_toggle, name='follow_toggle'),
    url(r'^facebook-login/$', views.facebook_login, name='facebook_login'),
    url(r'^front-facebook-login/$', views.FrontFacebookLogin.as_view(), name='front-facebook-login'),
]
