from django.conf.urls import url

from post.views import (
    post_list, comment_add, post_add, comment_delete,
    post_delete, post_detail, post_like,
)

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'detail/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'(?P<pk>\d+)/comment/add/$', comment_add, name='comment_add'),
    url(r'(?P<pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', comment_delete, name='comment_delete'),
    url(r'post-add/$', post_add, name='post_add'),
    url(r'post-delete/(?P<pk>\d+)/$', post_delete, name='post_delete'),
    url(r'^like/(?P<pk>\d+)/$', post_like, name='post_like'),
]