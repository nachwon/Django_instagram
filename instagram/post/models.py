from django.conf import settings
from django.db import models


class SubRelation(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following')

    def __str__(self):
        return f'{self.follower.username} is following {self.following.username}'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post')
    content = models.TextField(blank=True, null=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='liked_posts',
    )
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


class PostLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} liked Post {self.post.pk}'

    class Meta:
        ordering = ["liked_date"]





