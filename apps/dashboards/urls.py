from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [    
    path('departments/performance/', views.DepartmentsRatingView.as_view()),
    path('organization/data/', views.OrganizationalView.as_view()),
    path('department/overview/', views.DepartmentalOverviewView.as_view()), 
    path('department/competencies/', views.DepartmentalCompetenciesView.as_view()),    
]