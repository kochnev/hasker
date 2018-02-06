from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label='Email', help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'avatar' )
        labels = {
            'username': 'Login',
            'email': 'Email',
            'password1': 'Password',
            'avatar': 'Avatar'
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Repeat Password'


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'avatar')
        labels = {
            'email': 'Email',
            'avatar': 'Avatar',
        }