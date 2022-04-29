from django.test import TestCase
from ..models import Post, User
from django.db import models

class TestModels(TestCase):

    def setUp(self):

        testUser = User.objects.create_user(username="testUser", email="email@mail.com", password="testpass")

        self.post1 = Post.objects.create(
            author = testUser,
            title = 'test',
            description = 'testing',
            created_at = models.DateTimeField(auto_now=True),
            updated_at = models.DateTimeField(auto_now=True),
        )

    def test_creation_of_post(self):
        self.assertEquals(self.post1.title, 'test')


