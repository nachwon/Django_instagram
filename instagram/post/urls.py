from django.conf.urls import url

from post.views import post_list, comment_add, post_add, comment_delete, post_delete, post_edit

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'(?P<pk>\d+)/comment/add/$', comment_add, name='comment_add'),
    url(r'(?P<pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', comment_delete, name='comment_delete'),
    url(r'add/$', post_add, name='post_add'),
    url(r'delete/(?P<pk>\d+)/$', post_delete, name='post_delete'),
    url(r'edit/(?P<pk>\d+)/$', post_edit, name='post_edit'),
]