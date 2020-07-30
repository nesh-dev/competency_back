from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Competency,Strands,AssessmentModel
from .serializer import CompetencySerializer,StrandsSerializer,AssessmentSerializer

from apps.reportee.models import ReporteeProfile
from apps.manager.models import ManagerProfile
from apps.supervisor.models import SupervisorProfile
from django.contrib.auth import get_user_model as user_model
User = user_model()

# Create your views here.
class CompetencyList(APIView):
    def get(self, request, format=None):
        competency = Competency.objects.all()
        serializers = CompetencySerializer(competency, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = CompetencySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetencyUpdate(APIView):

    def get_competency(self, pk):
        try:
            return Competency.objects.get(id=pk)
        except Competency.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        competency = self.get_competency(pk)
        serializers = CompetencySerializer(competency)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        competency = self.get_competency(pk)
        serializers = CompetencySerializer(competency, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        competency = self.get_competency(pk)
        competency.delete()
        return_message = {'message':"Competency deleted successful",}
        return Response(return_message, status=status.HTTP_204_NO_CONTENT)


class StrandsList(APIView):
            
    def get(self, request, format=None):
        strands = Strands.objects.all()
        serializers = StrandsSerializer(strands, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = StrandsSerializer(data=request.data, partial=True)
        if serializers.is_valid():
            this_competency_id = int(serializers.validated_data['competency_num'])
            this_competency = Competency.objects.get(pk=this_competency_id)
            serializers.save(competency=this_competency)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class StrandsUpdate(APIView):

    def get_strand(self, pk):
        try:
            return Strands.objects.get(id=pk)
        except Strands.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        strand = self.get_strand(pk)
        serializers = StrandsSerializer(strand)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        strand = self.get_strand(pk)
        serializers = StrandsSerializer(strand, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        strand = self.get_strand(pk)
        strand.delete()
        return_message = {'message':"Strand deleted successful",}
        return Response(return_message, status=status.HTTP_204_NO_CONTENT)

class CompetencyStrands(APIView):

    def get(self, request, id, format=None):
        strands = Strands.objects.filter(competency = id)
        serializers = StrandsSerializer(strands, many=True)
        return Response(serializers.data)

class AssessmentList(APIView):
    def get(self, request, format=None):
        assessments = AssessmentModel.objects.all()
        serializers = AssessmentSerializer(assessments, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = AssessmentSerializer(data=request.data, partial= True)
        if serializers.is_valid():
            this_assesser_id = int(serializers.validated_data['assessing_num'])
            this_assessee_id = int(serializers.validated_data['assessed_num'])
            this_strands_id = int(serializers.validated_data['strands_num'])
            assess_value = int(serializers.validated_data['value'])
            this_strands = Strands.objects.get(pk=this_strands_id)
            this_assesser = User.objects.get(pk=this_assesser_id)
            this_assessee = User.objects.get(pk=this_assessee_id)
            serializers.save(person_assessing=this_assesser, person_assessed= this_assessee, value = assess_value, strands = this_strands )
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SelfAssessment(APIView):

    def get_self_assessment(self, pk):
        try:
            return AssessmentModel.objects.filter(person_assessed=pk).order_by('-created_at')
        except Strands.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        assessments = self.get_self_assessment(pk)
        serializers = AssessmentSerializer(assessments, many= True)
        return Response(serializers.data)

class AssesserAssessment(APIView):

    def get_assesser_assessment(self, pk):
        try:
            return AssessmentModel.objects.filter(person_assessing=pk).order_by('-created_at')
        except Strands.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        assessments = self.get_assesser_assessment(pk)
        serializers = AssessmentSerializer(assessments, many= True)
        return Response(serializers.data)
