from django.conf.urls import url

from dashboard.views.admin_dashboard import AdminDashboardView
from dashboard.views.calendar import CalendarView
from dashboard.views.dashboardView import DashboardView
from dashboard.views.document import DocumentListView, DocumentCreateView, DocumentDetailView
from dashboard.views.home import AboutUs
from dashboard.views.implementing_partner import IPListView, IPCreateView, IPDetailView, IPFilterView, IPDeleteView
from dashboard.views.map import MapView
from dashboard.views.meeting import MeetingCreateView, MeetingAddAttendeesView, MeetingAttendeeDeleteView, \
    MeetingAttendeesNotifyView, MeetingListView, MeetingDeleteView
from dashboard.views.members import MemberCreateView, MemberListView, MemberDeleteView
from dashboard.views.task import TaskCreateView, TaskListView, TaskItemCreateView, TaskDetailView, TaskItemUpdateView, \
    TaskNoteUpdateView, TaskItemNotesListView, TaskUpdateView, TaskDeleteView, TaskFilter, TaskPopUpItem
from dashboard.views.upload import UploadView, XlsList
from dashboard.views.users import UserCreateView, UserListView, UserDeleteView, UserUpdateView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='home'),
    url(r'^about/$', AboutUs.as_view(), name='about-us'),

    url(r'^document/list/$', DocumentListView.as_view(), name='document-list'),
    url(r'^document/new/$', DocumentCreateView.as_view(), name='document-new'),
    url(r'^document/(?P<pk>\d+)/$', DocumentDetailView.as_view(), name='document-detail'),

    url(r'^dashboard/admin/$', AdminDashboardView.as_view(), name='admin'),

    url(r'^user/new/$', UserCreateView.as_view(), name='user-new'),
    url(r'^user/list/$', UserListView.as_view(), name='user-list'),
    url(r'^user/delete/(?P<pk>\d+)/$', UserDeleteView.as_view(), name='user-delete'),
    url(r'^user/edit/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-edit'),

    url(r'^task/new/$', TaskCreateView.as_view(), name='task-new'),
    url(r'^task/list/$', TaskListView.as_view(), name='task-list'),
    url(r'^task/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task-detail'),
    url(r'^task/edit/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='task-edit'),
    url(r'^task/delete/(?P<pk>\d+)/$', TaskDeleteView.as_view(), name='task-delete'),
    url(r'^task/filter/(?P<type>\w+)/$', TaskFilter.as_view(), name='task-filter'),
    url(r'^task/filter/(?P<type>\w+)/(?P<district>\w+)$', TaskPopUpItem.as_view(), name='task-filter'),

    url(r'^task/(?P<pk>\d+)/additems$', TaskItemCreateView.as_view(), name='task-add-items'),
    url(r'^task/item/(?P<pk>\d+)/update', TaskItemUpdateView.as_view(), name='task-update-items'),
    url(r'^task/note/(?P<pk>\d+)/update', TaskNoteUpdateView.as_view(), name='task-update-notes'),
    url(r'^item/(?P<pk>\d+)/notes', TaskItemNotesListView.as_view(), name='subtask-notes-list'),

    url(r'^upload/$', UploadView.as_view(), name='upload-docs'),
    url(r'^list/xls/$', XlsList.as_view(), name='list-xls'),


    url(r'^ip/list/$', IPListView.as_view(), name='ip-list'),
    url(r'^ip/new/$', IPCreateView.as_view(), name='ip-new'),
    url(r'^ip/delete/(?P<pk>\d+)/$', IPDeleteView.as_view(), name='ip-delete'),
    url(r'^ip/(?P<pk>\d+)/$', IPDetailView.as_view(), name='ip-detail'),
    url(r'^ip/(?P<pk>\d+)/districts/$', IPFilterView.as_view(), name='ip-filter'),

    url(r'^meeting/new/$', MeetingCreateView.as_view(), name='meeting-new'),
    url(r'^meeting/list/$', MeetingListView.as_view(), name='meeting-list'),
    url(r'^meeting/delete/(?P<pk>\d+)$', MeetingDeleteView.as_view(), name='meeting-delete'),
    url(r'^meeting/(?P<pk>\d+)/attendees/$', MeetingAddAttendeesView.as_view(), name='meeting-add-attendees'),
    url(r'^meeting/(?P<pk>\d+)/notify/$', MeetingAttendeesNotifyView.as_view(), name='meeting-notify-attendees'),
    url(r'^(?P<meeting_id>\d+)/attendees/(?P<pk>\d+)/delete/$', MeetingAttendeeDeleteView.as_view(),
        name='meeting-remove-attendees'),
    url(r'^calendar/$', CalendarView.as_view(), name='calendar-view'),

    url(r'^member/new/$', MemberCreateView.as_view(), name='member-new'),
    url(r'^member/list/$', MemberListView.as_view(), name='member-list'),
    url(r'^member/delete/(?P<pk>\d+)/$', MemberDeleteView.as_view(), name='member-delete'),


    url(r'^map/$', MapView.as_view(), name='map-view'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
]
