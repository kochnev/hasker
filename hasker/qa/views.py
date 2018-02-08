from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import QuestionForm, AnswerForm
from .models import Answer, Question, Tag


def index(request):
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 20)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'qa/index.html', {'questions': questions})


@login_required()
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.author = request.user
            q.save()
            q.tags.clear()
            tags_str = request.POST.get('tags')
            if tags_str:
                tags_arr = tags_str.split(',')
                for tag in tags_arr:
                    (t,created) = Tag.objects.get_or_create(title=tag)
                    t.save()
                    q.tags.add(t)
            q.save()

            return redirect('answer', q.slug)
    else:
        form = QuestionForm()

    return render(request, 'qa/add_question.html', {'form': form})


@login_required
def question_detail(request, slug):
    q = get_object_or_404(Question, slug=slug)
    answers = Answer.objects.filter(question=q)
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.author = request.user
            a.question = q
            a.save()
            return redirect('question_detail', q.slug)
    else:
        form = AnswerForm()

    return render(request, 'qa/question_detail.html', {'question': q, 'form': form, 'answers': answers})


@login_required
def mark_answer(request, slug, pk):
    a = get_object_or_404(Answer, pk=pk)
    a.is_correct = True
    a.save()
    return redirect('question_detail', slug)

