from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from dashboard.forms.users import UserForm
from dashboard.models import User
from dashboard.roles import IPUserRole


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        user = form.instance
        user.set_password(form.data.get('password'))
        user.save()
        IPUserRole.assign_role_to_user(user)
        # email = EmailMessage(
        #     'subject_message',
        #     'content_message',
        #     'sender smtp gmail' + '<chaimalariatool@gmail.com>',
        #     ['remo@codesync.ug'],
        #     headers={'Reply-To': 'chaimalariatool@gmail.com'}
        # )
        #
        # email.send(fail_silently=False)
        return super(UserCreateView, self).form_valid(form)


class UserListView(ListView):
    model = User

    class Meta:
        ordering = ["-id"]


class UserDeleteView(DeleteView):
    template_name = "dashboard/user_list.html"
    model = User
    success_url = reverse_lazy('dashboard:user-list')
