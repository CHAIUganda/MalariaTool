from django.contrib.sites.models import Site, RequestSite
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, DeleteView
from password_reset.utils import get_username

from dashboard.forms.users import UserForm
from dashboard.models import User
from dashboard.roles import IPUserRole


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = "/"
    email_template_name = 'dashboard/user_email.txt'
    email_subject_template_name = 'dashboard/user_email_subject.txt'

    def form_valid(self, form):
        user = form.instance
        user.set_password(form.data.get('password'))
        user.save()
        IPUserRole.assign_role_to_user(user)
        self.send_notification(user, form.data.get('password'))
        return super(UserCreateView, self).form_valid(form)

    def get_site(self):
        if Site._meta.installed:
            return Site.objects.get_current()
        else:
            return RequestSite(self.request)

    def send_notification(self, user, password):
        context = {
            'user': user,
            'site': self.get_site(),
            'pass': password,
            'username': get_username(user),
            'secure': self.request.is_secure(),
        }
        body = loader.render_to_string(self.email_template_name,
                                       context).strip()
        subject = loader.render_to_string(self.email_subject_template_name,
                                          context).strip()
        send_mail(subject, body, "National Malaria Control<me@remosamuel.com>",
                  [user.email])


class UserListView(ListView):
    model = User

    class Meta:
        ordering = ["-id"]


class UserDeleteView(DeleteView):
    template_name = "dashboard/user_list.html"
    model = User
    success_url = reverse_lazy('dashboard:user-list')
