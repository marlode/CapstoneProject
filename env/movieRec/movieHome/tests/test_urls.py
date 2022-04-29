from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import survey, sign_up, create_post, home


class TestsUrls(SimpleTestCase):

    def test_survey_url_is_resolved(self):
        url = reverse('survey')
        print(resolve(url))
        self.assertEquals(resolve(url).func, survey)

    def test_signup_url_is_resolved(self):
        url = reverse('sign_up')
        print(resolve(url))
        self.assertEquals(resolve(url).func, sign_up)
    
    def test_post_url_is_resolved(self):
        url = reverse('create_post')
        print(resolve(url))
        self.assertEquals(resolve(url).func, create_post)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)