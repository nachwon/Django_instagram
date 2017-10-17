from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post')
    content = models.TextField(blank=True, null=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_liked',)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.pk}'


class PostComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.post.pk} - Comment {self.pk}'

    class Meta:
        ordering = ["created_date"]





