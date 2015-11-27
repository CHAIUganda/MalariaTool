from django.views.generic import CreateView, ListView

from dashboard.forms.users import UserForm
from dashboard.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        user = form.instance
        user.set_password(form.data.get('password'))
        user.save()
        return super(UserCreateView, self).form_valid(form)


class UserListView(ListView):
    model = User
