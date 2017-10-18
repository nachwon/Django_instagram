from django.contrib import admin

from .models import Post, PostComment, PostLike, Subscribe, SubRelation

admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(Subscribe)
admin.site.register(SubRelation)
