from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import QuestionForm


class QATests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test',
                                        email='test@mail.ru',
                                        password='test123456789')
        user.save()




