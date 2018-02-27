from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import QuestionForm, AnswerForm
from .models import Answer, Question
from ..utils.paginator import paginate_list


def index(request):
    sort = request.GET.get('sort','id')
    question_list = Question.objects.all().order_by('-' + sort)
    page = request.GET.get('page')
    questions = paginate_list(question_list, page, 20)

    return render(request, 'qa/index.html', {'questions': questions})


@login_required()
def add_question(request):
    tags_str = ''
    tag_error = ''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        tags_str = request.POST.get('tags','')
        if form.is_valid():
            with transaction.atomic():
                q = form.save(commit=False)
                q.author = request.user
                q.save()
                tag_error = q.set_tags(tags_str=tags_str)
                if not tag_error:
                    return redirect('question_detail', q.slug)
    else:
        form = QuestionForm()

    return render(request, 'qa/add_question.html', {'form': form, 'tags': tags_str, 'tag_error': tag_error})


@login_required
def question_detail(request, slug):
    q = get_object_or_404(Question, slug=slug)
    answers_list = Answer.objects.filter(question=q).order_by('-rating','-created_at')
    page = request.GET.get('page')
    answers = paginate_list(answers_list, page, 20)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                a = form.save(commit=False)
                a.author = request.user
                a.question = q
                a.save()
                q.notify_answer_added(answer=a, link=request.build_absolute_uri())
            return redirect('question_detail', q.slug)
    else:
        form = AnswerForm()

    return render(request, 'qa/question_detail.html', {'question': q, 'form': form, 'answers': answers})


@login_required
def mark_answer(request, slug, pk):
    q = get_object_or_404(Question, slug=slug)
    a = get_object_or_404(Answer, pk=pk)
    q.correct_answer = a
    q.save()
    return redirect('question_detail', slug)


@login_required
def vote_question(request, slug, vote_type):
    q = get_object_or_404(Question, slug=slug)
    q.vote(request.user, int(vote_type))
    return redirect('question_detail', slug)


@login_required
def vote_answer(request, slug, pk, vote_type):
    a = get_object_or_404(Answer, pk=pk)
    a.vote(request.user, int(vote_type))
    return redirect('question_detail', slug)






