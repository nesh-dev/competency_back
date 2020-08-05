from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import DepartmentsRating, OrganizationalOverview, DepartmentalCompetencies, DepartmentalOverview
from apps.supervisor.models import Department
from apps.assessment.models import Competency


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = '__all__'

class DeptRatingSerializer(serializers.ModelSerializer):
    department = DepartmentsSerializer()
    
    class Meta:
        model = DepartmentsRating
        fields = '__all__'


class OrganizationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalOverview
        fields = '__all__'

class DeptOverviewSerializer(serializers.ModelSerializer):
    department = DepartmentsSerializer()
    class Meta:
        model = DepartmentalOverview
        fields = '__all__'

class DeptCompetenciesSerializer(serializers.ModelSerializer):
    department = DepartmentsSerializer()
    competency = CompetencySerializer()
    
    class Meta:
        model = DepartmentalCompetencies
        fields = '__all__'
