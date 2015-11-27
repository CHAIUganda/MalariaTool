from django.conf.urls import url

from dashboard.views.admin_dashboard import AdminDashboardView
from dashboard.views.document import DocumentListView, DocumentCreateView
from dashboard.views.home import Home
from dashboard.views.users import UserCreateView, UserListView

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^document/list/$', DocumentListView.as_view(), name='document-list'),
    url(r'^document/new/$', DocumentCreateView.as_view(), name='document-new'),
    url(r'^dashboard/admin/$', AdminDashboardView.as_view(), name='admin'),
    url(r'^user/new/$', UserCreateView.as_view(), name='add-user'),
    url(r'^user/list/$', UserListView.as_view(), name='list-user'),
]
