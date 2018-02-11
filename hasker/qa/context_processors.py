from .models import Question


def hot_questions(request):
    questions = Question.objects.all().order_by('-rating')[:20]
    return {'hot_questions': questions}
