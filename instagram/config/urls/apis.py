from django.conf.urls import url, include

urlpatterns = [
    url(r'^member/', include('member.urls.apis', namespace='api-member')),
    url(r'^post/', include('post.urls.apis', namespace='api-post')),
    # url(r'^utils/', include('utils.urls')),
    url(r'^sms/', include('sms.urls'))
]

