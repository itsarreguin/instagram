# Python standard library
from typing import Type

# Django imports
from django.test import TestCase
from django.test import Client
from django.urls import reverse

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile


class AccountViewsTestCase(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        self.feed_url = reverse('account:feed')
        self.login_url = reverse('account:login')
        self.sigup_url = reverse('account:signup')
        
        self.user: Type['User'] = User.objects.create_user(
            first_name='User',
            last_name='Test',
            username='testuser',
            email='usertest@example.com',
            password='!([p@SS-+w0rd)001}'
        )
    
    def test_signup_get(self) -> None:
        response = self.client.get(self.sigup_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 201)
        self.assertNotEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'auth/signup.html')
    
    def test_signup_post(self) -> None:
        response = self.client.post(
            path=self.sigup_url,
            data={
                'first_name': 'Another',
                'last_name': 'Test',
                'username': 'anothertest',
                'email': 'another_test@mydomain.com',
                'password': 'password1234'
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, self.feed_url)
    
    def test_login_get(self) -> None:
        response = self.client.get(self.login_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'auth/login.html')
    
    def test_login_post(self) -> None:
        response = self.client.post(
            path=self.login_url,
            data={'username': self.user.username, 'password': self.user.password}
        )
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, self.login_url)