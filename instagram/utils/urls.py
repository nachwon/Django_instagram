from django.conf.urls import url
from .apis import SendSMS

urlpatterns = [
    url(r'^sms/send/$', SendSMS.as_view(), name='post_list'),
]