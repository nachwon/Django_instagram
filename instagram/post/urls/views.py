from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'detail/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'post-add/$', views.post_add, name='post_add'),
    url(r'post-delete/(?P<pk>\d+)/$', views.post_delete, name='post_delete'),
    url(r'^like/(?P<pk>\d+)/$', views.post_like, name='post_like'),

    url(r'(?P<pk>\d+)/comment/add/$', views.comment_add, name='comment_add'),
    url(r'(?P<pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', views.comment_delete, name='comment_delete'),
]
