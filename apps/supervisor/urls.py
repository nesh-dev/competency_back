from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns=[
    path('supervisor/<int:pk>/', views.SupervisorProfileView.as_view()),
    path('departments/', views.DepartmentsView.as_view()),
    path('department/<int:pk>/', views.DepartmentView.as_view()),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)