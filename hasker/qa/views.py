from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Tag


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

            return redirect('index')
    else:
        form = QuestionForm()

    return render(request,
                  'qa/add_question.html',
                  {'form': form,})