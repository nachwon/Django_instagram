from django.db import models


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    content = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.pk}'


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.post.pk} - Comment {self.pk}'

    class Meta:
        ordering = ["created_date"]


