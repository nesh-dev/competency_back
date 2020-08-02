from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import ManagerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_name','email','is_supervisor','is_manager','is_reportee',)


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ManagerProfile
        fields = '__all__'
        
    