"""
SAM2017 URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^paper/', include('paper.urls', namespace='paper', app_name='paper')),
    url(r'^notification/', include('notification.urls', namespace='notification', app_name='notification')),
    url(r'^user_profile/$', include('user_profile.urls', namespace='user_profile', app_name='user_profile')),
    # url(r'^deadline/', include('deadline.urls', namespace='deadline', app_name='deadline')),
    url(r'^register/$', 'registration.views.register_user', name='registration'),
    url(r'^logout/$', views.logout_user, name='log_out'),
    url(r'rate_paper_pcm/', include('rate_paper_pcm.urls', namespace='rate_paper_pcm', app_name='rate_paper_pcm')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
