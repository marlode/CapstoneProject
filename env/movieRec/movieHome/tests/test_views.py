from cgi import test
import imp
from turtle import title
from django.forms import DateTimeField
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post, User
from django.db import models

class TestViews (TestCase):

    def setUp(self):
        self.client = Client()
        self.post_url = reverse('home')

        testUser = User.objects.create_user(username="testUser", email="email@mail.com", password="testpass")

        Post.objects.create(
            author = testUser,
            title = 'test',
            description = 'testing',
            created_at = models.DateTimeField(auto_now=True),
            updated_at = models.DateTimeField(auto_now=True),
        )

    def test_post_POST(self):
        response = self.client.post(self.post_url)
        self.assertEquals(response.status_code, 302)
        
