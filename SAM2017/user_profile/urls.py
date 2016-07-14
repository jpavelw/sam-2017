from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', 'user_profile.views.profile', name="user_profile"),
]
