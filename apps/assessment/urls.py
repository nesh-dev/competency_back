from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^competency/list/$', views.CompetencyList.as_view()),
    url(r'^competency/(\d+)/$', views.CompetencyUpdate.as_view()),
    url(r'^strands/list/$', views.StrandsList.as_view()),
    url(r'^strands/(\d+)/$', views.StrandsUpdate.as_view()),
    url(r'^competency/(\d+)/strands/$', views.CompetencyStrands.as_view()),
    url(r'^assessments/list/$', views.AssessmentList.as_view()),
    url(r'^assessee/(\d+)/$', views.SelfAssessment.as_view()),
    url(r'^assesser/(\d+)/$', views.AssesserAssessment.as_view()),
]
