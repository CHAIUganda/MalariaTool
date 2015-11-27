from django.conf.urls import url

from dashboard.views.admin_dashboard import AdminDashboardView
from dashboard.views.document import DocumentListView, DocumentCreateView, DocumentDetailView
from dashboard.views.home import Home
from dashboard.views.users import UserCreateView, UserListView

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^document/list/$', DocumentListView.as_view(), name='document-list'),
    url(r'^document/new/$', DocumentCreateView.as_view(), name='document-new'),
    url(r'^document/(?P<pk>\d+)/$', DocumentDetailView.as_view(), name='document-detail'),
    url(r'^dashboard/admin/$', AdminDashboardView.as_view(), name='admin'),
    url(r'^user/new/$', UserCreateView.as_view(), name='add-user'),
    url(r'^user/list/$', UserListView.as_view(), name='list-user'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
]
