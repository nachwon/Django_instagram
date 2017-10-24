from django.contrib.auth import authenticate
from django.test import TestCase, TransactionTestCase

from member.models import User


class UserModelTest(TransactionTestCase):
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'
    DUMMY_AGE = None

    def test_fields_default_value(self):
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, self.DUMMY_USERNAME)
        # self.assertEqual(user.img_profile, '')
        self.assertEqual(user.age, self.DUMMY_AGE)
        self.assertEqual(user.following.count(), 0)
        self.assertEqual(user, authenticate(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        ))

    def test_follow(self):
        mina, hyeri, yura, sojin = [User.objects.create_user(
            username=f'{name}',
            age=0,
        ) for name in ['Mina', 'Hyeri', 'Yura', 'Sojin']]

        mina.follow_toggle(hyeri)
        mina.follow_toggle(yura)
        mina.follow_toggle(sojin)

        hyeri.follow_toggle(yura)
        hyeri.follow_toggle(sojin)

        yura.follow_toggle(sojin)

        self.assertEqual(mina.following.count(), 3)
        self.assertEqual(hyeri.following.count(), 2)
        self.assertEqual(yura.following.count(), 1)
        self.assertEqual(sojin.following.count(), 0)

        self.assertIn(hyeri, mina.following.all())
        self.assertIn(yura, mina.following.all())
        self.assertIn(sojin, mina.following.all())

        self.assertIn(mina, hyeri.followers.all())
        self.assertIn(mina, yura.followers.all())
        self.assertIn(mina, sojin.followers.all())
