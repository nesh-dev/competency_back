from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.manager.models import ManagerProfile

from .models import SupervisorProfile, Department
from .serializer import SupervisorSerializer, DepartmentSerializer

# Create your views here.
class SupervisorProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()       
    
    def get_supervisor(self, pk):
        try:
            return SupervisorProfile.objects.get(pk=pk)
        except SupervisorProfile.DoesNotExist:
            raise Http404()
    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_supervisor = self.get_supervisor(pk)
        serializers = SupervisorSerializer(this_supervisor)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_supervisor = self.get_supervisor(pk)
        serializers = SupervisorSerializer(this_supervisor, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_supervisor = self.get_supervisor(pk)
        this_supervisor.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DepartmentsView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()    

    def get(self, request, format=None):
        self.check_role(request)
        all_departments = Department.objects.all()
        serializers = DepartmentSerializer(all_departments, many=True)
        return Response(serializers.data) 

    def post(self, request, format=None):
        self.check_role(request)
        serializers = DepartmentSerializer(data=request.data, partial=True)
        if serializers.is_valid():
            this_manager_id = int(serializers.validated_data['manager_id_num'])
            this_manager = ManagerProfile.objects.get(pk=this_manager_id)
            serializers.save(manager=this_manager)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager:
            pass
        else:
            raise Http404()       
    
    def get_department(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404()
    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_department = self.get_department(pk)
        serializers = DepartmentSerializer(this_department)
        return Response(serializers.data)


    def put(self, request, pk, format=None):
        self.check_role(request)
        this_department = self.get_department(pk)
        serializers = DepartmentSerializer(this_department, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_department = self.get_department(pk)
        this_department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)