from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photo')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PostComment:
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
