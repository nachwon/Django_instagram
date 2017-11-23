import filecmp
import io
from random import randint

import os
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from io import BytesIO
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APILiveServerTestCase, force_authenticate

from config import settings
from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'post:api_post_list'
    URL_API_POST_LIST = '/api/posts/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username)

    @staticmethod
    def create_post(author=None):
        f = File(BytesIO())
        Post.objects.create(photo=f, author=author)

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve(self):
        resolve_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolve_match.url_name, self.URL_API_POST_LIST_NAME)
        self.assertEqual(resolve_match.func.view_class,
                         self.VIEW_CLASS)

    def test_get_post_list(self):
        num = randint(0, 20)
        user = self.create_user()
        for i in range(num):
            self.create_post(author=user)

        url = reverse(self.URL_API_POST_LIST_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), num)
        self.assertEqual(len(response.data), num)

        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_date', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

    def test_api_post(self):
        factory = APIRequestFactory()
        user = self.create_user()
        f = os.path.join(settings.MEDIA_ROOT, 'post', 'favicon.png')
        with open(f, 'rb') as photo:
            request = factory.post('/api/posts/', {'content': 'hello', 'photo': photo})
        force_authenticate(request, user=user)

        view = PostList.as_view()
        response = view(request)

        print(response.data)

        test_user = User.objects.get(pk=1)

        self.assertEqual(response.data['content'], 'hello')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], test_user.pk)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.get(pk=response.data['pk'])
        self.assertTrue(filecmp.cmp(f, post.photo.file.name))


