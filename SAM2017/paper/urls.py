from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit$', views.submit, name="submit"),
    url(r'^submit/(?P<paper_id>[0-9]+)/', views.submit_file, name="submit_file"),
    url(r'^update/(?P<paper_id>[0-9]+)/$', views.update, name="update"),
    url(r'^submissions/(?P<paper_id>[0-9]+)/$', views.submissions, name="submissions"),
    url(r'^choose_paper$', views.choose_paper, name="choose_paper"),
    url(r'^chosen_papers$', views.chosen_papers, name="chosen_papers"),
    url(r'^my_papers/$', views.paper_listing, name="paper_listing"),
    url(r'^assign_paper/$',views.assign_paper,name="assign_paper"),
    url(r'^assign_pcm/(?P<paper_id>[0-9]+)/$', views.assign_pcm, name="assign_pcm"),
    url(r'^review_paper/$',views.review_paper,name="review_paper"),
]
