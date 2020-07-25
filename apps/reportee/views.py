from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ReporteeProfile
from .serializer import ReporteeSerializer

# Create your views here.
class ReporteeProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager or request.user.is_reportee:
            pass
        else:
            raise Http404()       
    
    def get_reportee(self, pk):
        try:
            return ReporteeProfile.objects.get(pk=pk)
        except ReporteeProfile.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_reportee = self.get_reportee(pk)
        serializers = ReporteeSerializer(this_reportee)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_reportee = self.get_reportee(pk)
        serializers = ReporteeSerializer(this_reportee, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_reportee = self.get_reportee(pk)
        this_reportee.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReporteesView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager:
            pass
        else:
            raise Http404()    

    def get(self, request, format=None):
        self.check_role(request)
        all_reportees = ReporteeProfile.objects.all()
        serializers = ReporteeSerializer(all_reportees, many=True)
        return Response(serializers.data) 