from django.test import TestCase


class PostLikeToggleViewTest(TestCase):
    def test_uses_post_like_toggle_view_template(self):
        response = self.client.get()
