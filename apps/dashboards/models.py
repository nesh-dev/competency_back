from django.db import models
from apps.supervisor.models import Department
from apps.assessment.models import Competency

# Create your models here.
class DepartmentsRating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)
    percent_progress = models.IntegerField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True)   

    def __str__(self):
        return self.department.department_name

class OrganizationalOverview(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    completed_assessments = models.IntegerField(blank=True)
    num_of_departments = models.IntegerField(blank=True)
    expected_assessments = models.IntegerField(blank=True)
    pending_assessments = models.IntegerField(blank=True)    

    def __str__(self):
        return f"Organizational overview"

class DepartmentalOverview(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True) 
    completed_assessments = models.IntegerField(blank=True)
    expected_assessments = models.IntegerField(blank=True)
    pending_assessments = models.IntegerField(blank=True)  
    department = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)  

    def __str__(self):
        return f"Departemental overview"

class DepartmentalCompetencies(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    competency = models.ForeignKey(Competency,on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.competency.name

