from django.conf.urls import url
from dhisdash.views import HomePageView, JsonDataView, JsonDistrictsView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^data.json$', JsonDataView.as_view(), name='json_data'),
    url(r'^districts.json$', JsonDistrictsView.as_view(), name='json_data'),

]