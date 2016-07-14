from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.rate_paper_pcm, name='rate_paper_pcm'),
    url(r'^paper/(?P<paper_id>[0-9]+)/$', views.rate_paper_pcm_input_form, name='rate_paper_pcm_input_form'),
    url(r'^reviewed_papers/$', views.reviewed_papers,name='reviewed_papers'),
    url(r'^reviewed_papers/(?P<paper_id>[0-9]+)/$', views.pcc_rate_paper,name='pcc_rate_paper'),
    url(r'^resolve_conflict/(?P<paper_id>[0-9]+)/$',views.resolve_paper_conflict,name='resolve_paper_conflict'),
]