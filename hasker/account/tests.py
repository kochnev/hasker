from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse



class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test',
                                        email='test@mail.ru',
                                        password='test123456789')
        user.save()

    def setUp(self):
        self.credentials = {'username': 'test1', 'password1': 'test123456789',
                            'password2': 'test123456789', 'email': 'test@mail.ru'}

    def test_view_renders(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_create_user(self):
        expected_username = self.credentials['username']
        self.client.post(reverse('signup'), self.credentials)
        self.assertTrue(get_user_model().objects.filter(username=expected_username).exists(),
                        "User was not created.")

    def test_password_required(self):
        params = self.credentials
        params.pop('password1')
        response = self.client.post(reverse('signup'), params)
        self.assertFormError(response, 'user_form', 'password1', 'This field is required.')

    def test_login(self):
        login = self.client.login(username='test', password='test123456789')
        resp = self.client.get(reverse('index'))
        self.assertEqual(str(resp.context['user']), 'test')

    def test_redirect_settings_if_not_logged_in(self):
        resp = self.client.get(reverse('settings'))
        self.assertRedirects(resp, '/login/?next=/settings/')


