from django.conf.urls import url

from dashboard.views.admin_dashboard import AdminDashboardView
from dashboard.views.calendar import CalendarView
from dashboard.views.document import DocumentListView, DocumentCreateView, DocumentDetailView
from dashboard.views.home import Home
from dashboard.views.implementing_partner import IPListView, IPCreateView, IPDetailView
from dashboard.views.task import TaskCreateView, TaskListView, TaskItemCreateView
from dashboard.views.users import UserCreateView, UserListView

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),

    url(r'^document/list/$', DocumentListView.as_view(), name='document-list'),
    url(r'^document/new/$', DocumentCreateView.as_view(), name='document-new'),
    url(r'^document/(?P<pk>\d+)/$', DocumentDetailView.as_view(), name='document-detail'),

    url(r'^dashboard/admin/$', AdminDashboardView.as_view(), name='admin'),

    url(r'^user/new/$', UserCreateView.as_view(), name='user-new'),
    url(r'^user/list/$', UserListView.as_view(), name='user-list'),

    url(r'^task/new/$', TaskCreateView.as_view(), name='task-new'),
    url(r'^task/list/$', TaskListView.as_view(), name='task-list'),
    url(r'^task/(?P<pk>\d+)/additems$', TaskItemCreateView.as_view(), name='task-add-items'),

    url(r'^ip/list/$', IPListView.as_view(), name='ip-list'),
    url(r'^ip/new/$', IPCreateView.as_view(), name='ip-new'),
    url(r'^ip/(?P<pk>\d+)/$', IPDetailView.as_view(), name='ip-detail'),

    url(r'^calendar/$', CalendarView.as_view(), name='calendar-view'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
]
