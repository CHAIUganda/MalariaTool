from django.core.mail import EmailMessage
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):

        return super(LoginView, self).get(request, *args, **kwargs)
