from django.contrib import admin
from .models import OrganizationalOverview,DepartmentalOverview,DepartmentalCompetencies,DepartmentsRating

# Register your models here.
admin.site.register(OrganizationalOverview)
admin.site.register(DepartmentsRating)
admin.site.register(DepartmentalOverview)
admin.site.register(DepartmentalCompetencies)
