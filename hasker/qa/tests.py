from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from .models import Question
from .forms import QuestionForm


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

    def test_question_form_empty_title(self):
        form_data = {'text': 'question text'}
        form = QuestionForm(form_data)
        self.assertFalse(form.is_valid())

    def test_question_form_empty_text(self):
        form_data = {'title': 'question title'}
        form = QuestionForm(form_data)
        self.assertFalse(form.is_valid())

    def test_question_form_up_to_three_tags(self):
        self.client.login(username='test1', password='test123456789')
        resp = self.client.post(reverse('add_question'), {'title': 'title question',
                                                          'text': 'text question',
                                                          'tags': 'books,music,football,swimming'})
        self.assertNotEqual(resp.context['tag_error'], '')










