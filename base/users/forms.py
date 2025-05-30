from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(UserCreationForm):
    command = forms.BooleanField()
    command.label = 'Зарегистрироваться как команда'
    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields["password2"].required = False
        self.fields["command"].required = False