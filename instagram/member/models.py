from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True)
    img_profile = models.ImageField(
        '프로필 사진',
        upload_to='user',
        default='user/default-profile.png',
        blank=True,
    )
    age = models.IntegerField('나이', null=True)
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_CHOICES = {
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    }
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=USER_TYPE_DJANGO
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relationship',
        related_name='followers',
        verbose_name='팔로우 유저',
        blank=True,
    )

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError()
        relation, relation_created = self.following_set.get_or_create(to_user=user)
        if relation_created:
            return f'{self.username} followed {user.username}'
        relation.delete()
        return f'{self.username} unfollowed {user.username}'


class Relationship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following_set')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='follower_set')
    related_date = models.DateTimeField(auto_now_add=True)
    RELATION_TYPE_CHOICES = (
        ('Block', 'Block',),
        ('Close', 'Close',),
        ('Acquaintance', 'Acquaintance',),
    )
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPE_CHOICES)

    def __str__(self):
        if self.relation_type == 'Block':
            return f'{self.from_user} blocked {self.to_user}'
        else:
            return f'{self.from_user} is following {self.to_user}'
