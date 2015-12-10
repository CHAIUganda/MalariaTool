from django.forms import ModelForm

from dashboard.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['title', 'first_name', 'last_name', 'password', 'email', 'ip']
