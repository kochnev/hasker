from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label='Email', help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        labels = {
            'username': 'Login',
            'email': 'Email',
            'password1': 'Password',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Repeat Password'


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        labels = {
            'email': 'Email',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
        labels = {
            'avatar': 'Avatar',
        }
