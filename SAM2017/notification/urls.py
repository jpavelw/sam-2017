from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notification/$', views.notifications, name='notification'),
    url(r'^delete/(?P<notification_id>[0-9]+)/$', views.delete_notification, name='delete_notification'),
]