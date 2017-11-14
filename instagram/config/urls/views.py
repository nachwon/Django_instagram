from django.conf.urls import url, include

from django.contrib import admin

from config.views import redirect_to_main


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', redirect_to_main, name='index'),
    url(r'^post/', include('post.urls.views', namespace='post')),
    url(r'^member/', include('member.urls.views', namespace='member')),
]
