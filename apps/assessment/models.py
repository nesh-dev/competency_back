from django.db import models
from django.contrib.auth import get_user_model as user_model
User = user_model()

from apps.reportee.models import ReporteeProfile
from apps.manager.models import ManagerProfile
from apps.supervisor.models import SupervisorProfile

class Competency(models.Model):
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Strands(models.Model):
    name = models.CharField(max_length=60)
    competency = models.ForeignKey(Competency,on_delete=models.CASCADE)
    competency_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

class AssessmentModel(models.Model):
    strands = models.ForeignKey(Strands,on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency,on_delete=models.CASCADE)
    person_assessing = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assesser')
    person_assessed = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assessee')
    competency_num = models.IntegerField()
    strands_num = models.IntegerField()
    assessing_num = models.IntegerField()
    assessed_num = models.IntegerField()
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SelfAssessmentAverage(models.Model):
    competency = models.ForeignKey(Competency,on_delete=models.CASCADE)
    assessee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assessee_average')
    assessee_num = models.IntegerField()
    competency_num = models.IntegerField()
    average = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

class PersonAssessingAverage(models.Model):
    competency = models.ForeignKey(Competency,on_delete=models.CASCADE)
    assessee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assesser_average')
    assessee_num = models.IntegerField()
    competency_num = models.IntegerField()
    average = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
