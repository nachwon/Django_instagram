from django.conf.urls import url
from .apis import SendSMS

urlpatterns = [
    url(r'^send/$', SendSMS.as_view(), name='sms'),
]