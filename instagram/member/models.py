from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 사진',
        upload_to='user',
        default='/media/default-profile.jpg',
        blank=True,
    )
    age = models.IntegerField('나이', null=True)
    user = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_user',
        verbose_name='팔로우 유저',
        blank=True,
    )

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
