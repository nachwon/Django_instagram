import io
from random import randint

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse, resolve
from io import BytesIO
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APILiveServerTestCase

from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'post_list'
    URL_API_POST_LIST = '/api/posts/'
    VIEW_CLASS = PostList

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
        f = File(BytesIO())
        user = User.objects.create_user(username='che1')
        for i in range(num):
            Post.objects.create(photo=f, author=user)
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




