from django.conf.urls import url

from post.views import post_list, comment_add, post_add

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'(?P<pk>\d+)/$', comment_add, name='comment_add'),
    url(r'add/$', post_add, name='post_add'),
]