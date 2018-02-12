from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import QuestionForm, AnswerForm
from .models import Answer, Question, Tag


def index(request):
    sort = request.GET.get('sort','id')
    question_list = Question.objects.all().order_by('-' + sort)
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
    tags_str = ''
    tag_error = ''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        tags_str = request.POST.get('tags')
        if form.is_valid():
            q = form.save(commit=False)
            q.author = request.user
            q.save()
            if tags_str:
                tags_arr = tags_str.split(',')
                if len(tags_arr) <= 3:
                    for tag in tags_arr:
                        (t,created) = Tag.objects.get_or_create(title=tag)
                        t.save()
                        q.tags.add(t)
                    q.save()
                    return redirect('question_detail', q.slug)
                else:
                    tag_error = 'You are allowed to input up to 3 tags'
    else:
        form = QuestionForm()

    return render(request, 'qa/add_question.html', {'form': form, 'tags': tags_str, 'tag_error': tag_error})


@login_required
def question_detail(request, slug):
    q = get_object_or_404(Question, slug=slug)
    answers_list = Answer.objects.filter(question=q).order_by('-rating','-created_at')
    paginator = Paginator(answers_list, 30)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)

    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.author = request.user
            a.question = q
            a.save()
            send_mail(
                'new answer was added',
                'The answer is:\n' +
                 a.text + '\n\n' +
                'Here is the link for your question ' + request.build_absolute_uri(),
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
            return redirect('question_detail', q.slug)
    else:
        form = AnswerForm()

    return render(request, 'qa/question_detail.html', {'question': q, 'form': form, 'answers': answers})


@login_required
def mark_answer(request, slug, pk):
    q = get_object_or_404(Question, slug=slug)
    Answer.objects.filter(question=q).update(is_correct=None)
    a = get_object_or_404(Answer, pk=pk)
    a.is_correct = True
    a.save()
    q.has_answer = True
    q.save()
    return redirect('question_detail', slug)


@login_required
def vote_question(request, slug, type_vote):
    q = get_object_or_404(Question, slug=slug)
    user = request.user
    if type_vote == 'up':
        q.upvote(user)
    elif type_vote == 'down':
        q.downvote(user)
    elif type_vote == 'cancel':
        q.cancel_vote(user)
    return redirect('question_detail', slug)

@login_required
def vote_answer(request, slug, pk, type_vote):
    a = get_object_or_404(Answer, pk=pk)
    user = request.user
    if type_vote == 'up':
        a.upvote(user)
    elif type_vote == 'down':
        a.downvote(user)
    elif type_vote == 'cancel':
        a.cancel_vote(user)
    return redirect('question_detail', slug)






