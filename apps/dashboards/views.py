from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import DepartmentsRating, OrganizationalOverview, DepartmentalOverview, DepartmentalCompetencies
from .serializer import DeptRatingSerializer, OrganizationalSerializer, DeptCompetenciesSerializer, DeptOverviewSerializer
from apps.reportee.models import ReporteeProfile
from apps.manager.models import ManagerProfile
from apps.supervisor.models import SupervisorProfile, Department
from apps.assessment.models import Competency,Strands,AssessmentModel

# Create your views here.
class DepartmentsRatingView(APIView):
    permission_classes = (IsAuthenticated,) 
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()      

    def get(self, request, format=None):   
        self.check_role(request)     
        departments = DepartmentsRating.objects.all()
        serializers = DeptRatingSerializer(departments, many=True)
        return Response(serializers.data)

class OrganizationalView(APIView):
    permission_classes = (IsAuthenticated,) 
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()      

    def get(self, request, format=None):   
        self.check_role(request)     
        organizational_data = OrganizationalOverview.objects.all()
        serializers = OrganizationalSerializer(organizational_data, many=True)
        return Response(serializers.data)

class DepartmentalOverviewView(APIView):
    permission_classes = (IsAuthenticated,) 
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager:
            pass
        else:
            raise Http404()      

    def get(self, request, format=None):   
        self.check_role(request)
        
        departments = Department.objects.all()
        all_strands = Strands.objects.all()
        num_of_strands = len(all_strands)
        for dept in departments:
            avg_list = []
            reportees = ReporteeProfile.objects.filter(department = dept)
            completed_assessments = 0
            for reportee in reportees:
                reportee_user = reportee.user
                assessements = AssessmentModel.objects.filter(person_assessed = reportee_user)
                if len(assessements)>=num_of_strands:
                    completed_assessments=completed_assessments+1
                for assessment in assessements:
                    avg_list.append(assessment.value)

            
            expected_assessments = len(reportees)
            pending_assessments = expected_assessments-completed_assessments
            
            overviews = DepartmentalOverview.objects.all()
            overview_list=[]
            for overview in overviews:
                overview_list.append(overview.department)
            if dept in overview_list:
                this_overview = DepartmentalOverview.objects.get(department = dept)
                this_overview.overall_rating = sum(avg_list)/len(avg_list)
                this_overview.completed_assessments = completed_assessments
                this_overview.pending_assessments = pending_assessments
                this_overview.expected_assessments =expected_assessments
                this_overview.save()
            else:
                new_overview = DepartmentalOverview()
                new_overview.department = dept
                new_overview.overall_rating = sum(avg_list)/len(avg_list)
                new_overview.completed_assessments = completed_assessments
                new_overview.pending_assessments = pending_assessments
                new_overview.expected_assessments =expected_assessments
                new_overview.save()


        departmental_data = DepartmentalOverview.objects.all()
        serializers = DeptOverviewSerializer(departmental_data, many=True)
        return Response(serializers.data)
    
class DepartmentalCompetenciesView(APIView):
    permission_classes = (IsAuthenticated,) 
    def check_role(self, request):
        if request.user.is_supervisor or request.user.is_manager:
            pass
        else:
            raise Http404()      

    def get(self, request, format=None):   
        self.check_role(request)

        departments = Department.objects.all()
        for dept in departments:            
            competencies = Competency.objects.all()            
            for competency in competencies:
                avg_list=[]
                strands = Strands.objects.filter(competency = competency)
                for strand in strands:
                    reportees = ReporteeProfile.objects.filter(department = dept)
                    for reportee in reportees:
                        reportee_user = reportee.user
                        assessments = AssessmentModel.objects.filter(person_assessed = reportee_user, strands = strand)
                        for assessment in assessments:
                            avg_list.append(assessment.value)
                competency_avg = sum(avg_list)/len(avg_list)
                all_comps = DepartmentalCompetencies.objects.filter(department = dept, competency =competency)
                if len(all_comps)>=1:
                    for comps in all_comps:
                        comps.avg_rating = competency_avg
                        comps.save()
                else:
                    this_comps = DepartmentalCompetencies()
                    this_comps.avg_rating = competency_avg
                    this_comps.department = dept
                    this_comps.competency = competency
                    this_comps.save()


        comps_data = DepartmentalCompetencies.objects.all()
        serializers = DeptCompetenciesSerializer(comps_data, many=True)
        return Response(serializers.data)
