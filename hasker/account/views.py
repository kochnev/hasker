from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = UserForm()
    return render(request, 'account/signup.html',
                      {'user_form': user_form,})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Пользователь заблокирован!')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Неверно введен логин или пароль!')
            return redirect('login')
    else:
        return render(request, 'account/login.html', {})

