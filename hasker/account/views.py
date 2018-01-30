from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, UserSettingsForm, UserProfileForm


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'account/signup.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


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


@login_required
def settings(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.INFO, 'Настройки успешно сохранены!')
            return redirect('settings')
    else:
        user_form = UserSettingsForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request,
                  'account/settings.html',
                  {})


