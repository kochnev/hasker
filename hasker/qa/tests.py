from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class QATests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test',
                                        email='test@mail.ru',
                                        password='test123456789')
        user.save()

    def test_pagination_question_list_is_twenty(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['questions']) == 20)




