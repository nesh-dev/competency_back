from rest_framework import serializers
from .models import Competency,Strands,AssessmentModel

class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = ('id','name','created_at', 'updated_at')

class StrandsSerializer(serializers.ModelSerializer):
    competency = CompetencySerializer()

    class Meta:
        model = Strands
        fields = '__all__'

class Strands2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Strands
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    strands = Strands2Serializer()

    class Meta:
        model = AssessmentModel
        fields = '__all__'

