from django.contrib import admin
from .models import AssessmentModel,Competency,Strands

# Register your models here.
admin.site.register(AssessmentModel)
admin.site.register(Competency)
admin.site.register(Strands)
