from django.shortcuts import render, redirect
from .forms import QuestionForm


def index(request):
    return render(
        request,
        'qa/index.html',
        {},
    )


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuestionForm()

    return render(request,
                  'qa/add_question.html',
                  {'form': form,})