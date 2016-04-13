from django.conf.urls import url
from django.views.generic import TemplateView
from dhisdash.views import HomePageView, JsonDataView, JsonDistrictsView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    # url(r'^about/$', TemplateView.as_view(template_name='dhisdash/about-us.html'), name='about-us'),
    url(r'^data.json$', JsonDataView.as_view(), name='json_data'),
    url(r'^districts.json$', JsonDistrictsView.as_view(), name='json_data'),

]