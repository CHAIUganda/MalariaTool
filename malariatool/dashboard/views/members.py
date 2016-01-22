from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from dashboard.models import Member


class MemberCreateView(CreateView):
    model = Member
    fields = ['title', 'first_name', 'last_name', 'profile_picture']
    success_url = reverse_lazy("dashboard:admin")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(MemberCreateView, self).form_valid(form)


class MemberListView(ListView):
    model = Member


class MemberDeleteView(DeleteView):
    model = Member
    success_url = reverse_lazy("dashboard:member-list")
