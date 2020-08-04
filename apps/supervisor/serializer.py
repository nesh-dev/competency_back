from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import SupervisorProfile, Department
from apps.manager.models import ManagerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_name','email','is_supervisor','is_manager','is_reportee',)

class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = ManagerProfile
        fields = '__all__'


class SupervisorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SupervisorProfile
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()

    class Meta:
        model = Department
        fields = '__all__'

        
    