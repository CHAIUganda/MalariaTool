"""malariatool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from password_reset import urls as password_urls
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from dashboard import urls as dashboard_urls
from dhisdash import urls as dhisdash_urls
from malariatool import settings

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^reset/', include(password_urls)),
                  url(r'^', include(dhisdash_urls, namespace='dhisdash')),
                  url(r'^', include(dashboard_urls, namespace='dashboard')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
