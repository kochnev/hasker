from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from .models import Question, Answer


class QATests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = get_user_model().objects.create_user(username='test1',
                                        email='test1@mail.ru',
                                        password='test123456789')

        user1.save()


        # create 30 Question
        for i in range(30):
            Question.objects.create(title='Question' + str(i), slug='question' + str(i),
                                    text='text of question' + str(i), author=user1)


    def test_pagination_question_list(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['questions']) == 20)






