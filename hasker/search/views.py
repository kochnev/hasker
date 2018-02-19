from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..qa.models import Question
from ..utils.paginator import paginate_list

QUERY_STRING_LIMIT = 128


def search(request):
    q = request.GET.get('q', '')
    q = (q[:QUERY_STRING_LIMIT]) if len(q) > QUERY_STRING_LIMIT else q
    if 'tag:' in q:
        tag = q.split(':')[1]
        return redirect('tag_search', tag)

    question_list = Question.objects.filter(Q(title__contains=q)|Q(text__contains=q)).order_by('-rating','created_at')
    page = request.GET.get('page')
    questions = paginate_list(question_list, page, 20)
    return render(request, 'search/search_result.html', {'questions': questions, 'q': q})


def tag_search(request, tag):
    question_list = Question.objects.filter(tags__title=tag).order_by('-rating', 'created_at')
    page = request.GET.get('page')
    questions = paginate_list(question_list, page, 20)
    return render(request, 'search/tag_result.html', {'questions': questions})

