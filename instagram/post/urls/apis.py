from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^api/posts/$', apis.PostList.as_view(), name='post_list'),
    url(r'^api/posts/(?P<pk>\d+)$', apis.PostDetail.as_view(), name='post_detail'),
]

