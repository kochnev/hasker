from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from ..qa.models import Question


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = get_user_model().objects.create_user(username='test1',
                                        email='test1@mail.ru',
                                        password='test123456789')
        user1.save()

        # create 30 Question
        for i in range(30):
            q = Question.objects.create(title='Question' + str(i), slug='question' + str(i),
                                    text='text of question' + str(i), author=user1)
            q.set_tags('books,music')

    def test_search_by_text(self):
        resp = self.client.get('%s?q=Quest' % reverse('search'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Quest', resp.context['questions'][0].title, )
        self.assertTrue(len(resp.context['questions']) == 20)

    def test_search_by_tag(self):
        resp = self.client.get(reverse('tag_search', args=['books']))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['questions']) == 20)
