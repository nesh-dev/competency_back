from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ManagerProfile
from .serializer import ManagerSerializer

# Create your views here.
class ManagerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager:
            pass
        else:
            raise Http404()       
    
    def get_manager(self, pk):
        try:
            return ManagerProfile.objects.get(pk=pk)
        except ManagerProfile.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_manager = self.get_manager(pk)
        serializers = ManagerSerializer(this_manager)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_manager = self.get_manager(pk)
        serializers = ManagerSerializer(this_manager, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_manager = self.get_manager(pk)
        this_manager.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManagersView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()    

    def get(self, request, format=None):
        self.check_role(request)
        all_managers = ManagerProfile.objects.all()
        serializers = ManagerSerializer(all_managers, many=True)
        return Response(serializers.data) 

    