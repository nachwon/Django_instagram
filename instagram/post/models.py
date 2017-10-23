from django.conf import settings
from django.db import models


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author=None)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    photo = models.ImageField(upload_to='post')
    content = models.TextField(blank=True, null=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='liked_posts',
    )
    created_date = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return f'Post {self.pk}'

    class Meta:
        ordering = ["-created_date"]


class PostComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.post.pk} - Comment {self.pk}'

    class Meta:
        ordering = ["created_date"]


class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} liked Post {self.post.pk}'

    class Meta:
        ordering = ["liked_date"]
