from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..qa.models import Question


def search(request):
    q = request.GET.get('q', '')
    if 'tag:' in q:
        tag = q.split(':')[1]
        return redirect('tag_search', tag)

    question_list = Question.objects.filter(Q(title__contains=q)|Q(text__contains=q)).order_by('-rating','created_at')
    paginator = Paginator(question_list, 20)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'search/search_result.html', {'questions': questions, 'q': q})


def tag_search(request, tag):
    question_list = Question.objects.filter(tags__title=tag).order_by('-rating', 'created_at')
    paginator = Paginator(question_list, 20)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'search/tag_result.html', {'questions': questions})

