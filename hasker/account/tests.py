from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import User


class SignUpTests(TestCase):
    def setUp(self):
        self.credentials = {'username': 'test', 'password1': 'test123456789',
                            'password2': 'test123456789', 'email': 'test@mail.ru'}

    def test_view_renders(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_create_user(self):
        expected_username = self.credentials['username']
        self.client.post(reverse('signup'), self.credentials)
        self.assertTrue(User.objects.filter(username=expected_username).exists(),
                        "User was not created.")

    def test_password_required(self):
        params = self.credentials.copy()
        params.pop('password1')
        response = self.client.post(reverse('signup'), params)
        self.assertFormError(response, 'user_form', 'password1', 'This field is required.')

