from django.test import TestCase
from django.urls import reverse

class AccountsAuthFlowTests(TestCase):
    def test_register_login_profile_flow(self):
        # register
        resp = self.client.post(reverse('register'), {
            'username': 'alice',
            'email': 'alice@example.com',
            'password1': 'Astrong_pass123',
            'password2': 'Astrong_pass123',
        })
        self.assertRedirects(resp, reverse('profile'))

        # profile accessible
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Your Profile')

        # logout (POST)
        resp = self.client.post(reverse('logout'))
        self.assertRedirects(resp, reverse('login'))

        # login again
        resp = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'Astrong_pass123',
        })
        self.assertRedirects(resp, reverse('profile'))

    def test_profile_requires_login(self):
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)
