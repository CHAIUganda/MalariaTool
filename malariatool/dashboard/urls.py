from django.conf.urls import url

from dashboard.views.home import Home

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
]
