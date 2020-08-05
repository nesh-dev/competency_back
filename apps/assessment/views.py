from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Competency,Strands,AssessmentModel
from .serializer import CompetencySerializer,StrandsSerializer,AssessmentSerializer

from apps.reportee.models import ReporteeProfile
from apps.manager.models import ManagerProfile
from apps.supervisor.models import SupervisorProfile, Department
from django.contrib.auth import get_user_model as user_model
User = user_model()
from apps.dashboards.models import DepartmentsRating, OrganizationalOverview

# Create your views here.
class CompetencyList(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()  

    def get(self, request, format=None):        
        competency = Competency.objects.all()
        serializers = CompetencySerializer(competency, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        self.check_role(request)
        serializers = CompetencySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetencyUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404()  

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
        self.check_role(request)
        competency = self.get_competency(pk)
        serializers = CompetencySerializer(competency, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        competency = self.get_competency(pk)
        competency.delete()
        return_message = {'message':"Competency deleted successful",}
        return Response(return_message, status=status.HTTP_204_NO_CONTENT)


class StrandsList(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404() 
            
    def get(self, request, format=None):
        strands = Strands.objects.all()
        serializers = StrandsSerializer(strands, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        self.check_role(request)
        serializers = StrandsSerializer(data=request.data, partial=True)
        if serializers.is_valid():
            this_competency_id = int(serializers.validated_data['competency_num'])
            this_competency = Competency.objects.get(pk=this_competency_id)
            serializers.save(competency=this_competency)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class StrandsUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404() 

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
        self.check_role(request)
        strand = self.get_strand(pk)
        serializers = StrandsSerializer(strand, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        strand = self.get_strand(pk)
        strand.delete()
        return_message = {'message':"Strand deleted successful",}
        return Response(return_message, status=status.HTTP_204_NO_CONTENT)

class CompetencyStrands(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        strands = Strands.objects.filter(competency = id)
        serializers = StrandsSerializer(strands, many=True)
        return Response(serializers.data)

class AssessmentList(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_supervisor:
            pass
        else:
            raise Http404() 

    def get(self, request, format=None):
        self.check_role(request)
        assessments = AssessmentModel.objects.all()
        serializers = AssessmentSerializer(assessments, many=True)
        return Response(serializers.data) 

    def post(self, request, format=None):
        serializers = AssessmentSerializer(data=request.data, many=True,partial=True)
        if serializers.is_valid():
            this_assesser_id = int(serializers.validated_data['assessing_num'])
            this_assessee_id = int(serializers.validated_data['assessed_num'])
            this_strands_id = int(serializers.validated_data['strands_num'])
            this_competency_id = int(serializers.validated_data['competency_num'])
            assess_value = int(serializers.validated_data['value'])
            this_strands = Strands.objects.get(pk=this_strands_id)
            this_assesser = User.objects.get(pk=this_assesser_id)
            this_assessee = User.objects.get(pk=this_assessee_id)
            this_competency = Competency.objects.get(pk=this_competency_id)

            if this_assesser != this_assessee:
                try:
                    AssessmentModel.objects.get(person_assessing = this_assessee, person_assessed = this_assessee)
                except AssessmentModel.DoesNotExist:
                    message = {'error':"This user hasn't done a self-assessment yet",}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST) 
                except AssessmentModel.MultipleObjectsReturned: 
                    pass
                if this_assesser.is_supervisor and this_assessee.is_reportee: 
                    message = {'error':"A supervisor can't assess a reportee",}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST) 
                elif this_assesser.is_manager:
                    manager_profile = ManagerProfile.objects.get(user = this_assesser)     
                    manager_dept = Department.objects.get(manager = manager_profile)   
                    if manager_dept != this_assessee.reporteeprofile.department:
                        message = {'error':"The reportee is not in your department",}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST) 
            
            serializers.save(person_assessing=this_assesser, person_assessed= this_assessee, value = assess_value, strands = this_strands, competency = this_competency )


            # DepartmentsRatings
            if this_assessee.is_reportee:
                reportee_dept = this_assessee.reporteeprofile.department
                reportees_in_this_dept = ReporteeProfile.objects.filter(department = reportee_dept)
                avg_list = []
                for one_reportee in reportees_in_this_dept:
                    one_user = one_reportee.user
                    one_user_assessments = AssessmentModel.objects.filter(person_assessed=one_user)                    
                    for one_assessment in one_user_assessments:
                        avg_list.append(one_assessment.value)
                list_len = len(avg_list)
                dept_avg = sum(avg_list)/list_len

                completed_assessments = 0
                all_strands = Strands.objects.all()
                num_of_strands = len(all_strands)
                for one_reportee in reportees_in_this_dept:
                    one_user = one_reportee.user
                    one_user_assessments = AssessmentModel.objects.filter(person_assessed=one_user) 
                    if len(one_user_assessments)==num_of_strands*2:
                        completed_assessments = completed_assessments+1
                percent_progress = (completed_assessments/len(reportees_in_this_dept))*100

                recorded_departments = DepartmentsRating.objects.all()
                dept_list = []
                for dept in recorded_departments:
                    dept_list.append(dept.department)
                if reportee_dept in dept_list:
                    this_dept = DepartmentsRating.objects.get(department = reportee_dept)
                    this_dept.percent_progress = percent_progress
                    this_dept.rating = dept_avg
                    this_dept.save()
                else:
                    new_dept_rating = DepartmentsRating()
                    new_dept_rating.department = reportee_dept
                    new_dept_rating.percent_progress = percent_progress
                    new_dept_rating.rating = dept_avg
                    new_dept_rating.save()

            # OrganizationalOverview
            org_completed_assessments = 0
            all_reportees = ReporteeProfile.objects.all()
            for single_reportee in all_reportees:
                single_reportee_user = single_reportee.user
                single_reportee_assessments = AssessmentModel.objects.filter(person_assessed=single_reportee_user)
                all_strands = Strands.objects.all()
                num_of_strands = len(all_strands)
                if len(single_reportee_assessments)==num_of_strands*2:
                    org_completed_assessments=org_completed_assessments+1

            all_managers = ManagerProfile.objects.all()
            for single_manager in all_managers:
                single_manager_user = single_manager.user
                single_manager_assessments = AssessmentModel.objects.filter(person_assessed=single_manager_user)
                all_strands = Strands.objects.all()
                num_of_strands = len(all_strands)
                if len(single_manager_assessments)==num_of_strands*2:
                    org_completed_assessments=org_completed_assessments+1

            expected_assessments = len(all_reportees)+len(all_managers)
            pending_assessments = expected_assessments-org_completed_assessments
            
            num_of_departments = len(Department.objects.all())

            organizational_table = OrganizationalOverview.objects.all()
            if len(organizational_table)>0:
                for org in organizational_table:
                    org.completed_assessments = org_completed_assessments
                    org.num_of_departments = num_of_departments
                    org.expected_assessments = expected_assessments
                    org.pending_assessments = pending_assessments
                    org.save()
            else:
                this_organizational_table = OrganizationalOverview()
                this_organizational_table.completed_assessments = org_completed_assessments
                this_organizational_table.num_of_departments = num_of_departments
                this_organizational_table.expected_assessments = expected_assessments
                this_organizational_table.pending_assessments = pending_assessments
                this_organizational_table.save()
            
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SelfAssessment(APIView):
    permission_classes = (IsAuthenticated,)
    def validate_access(self, request, pk):
        if request.user.is_reportee:
            try:
                this_user = User.objects.get(id=pk)
            except User.DoesNotExist:
                raise Http404()
            if this_user == request.user:
                pass
            else:
                raise Http404()
        elif request.user.is_manager:
            try:
                this_user = User.objects.get(id=pk)
            except User.DoesNotExist:
                raise Http404()
            if this_user == request.user:
                pass
            elif this_user.is_reportee:
                manager_prof = ManagerProfile.objects.get(user = request.user)
                try:
                    manager_dept = Department.objects.get(manager = manager_prof)
                except Department.DoesNotExist:
                    raise Http404()
                if this_user.reporteeprofile.department == manager_dept:
                    pass
                else:
                    raise Http404()
            else:
                raise Http404()
        elif request.user.is_supervisor:
            pass
        else:
            raise Http404()

    def get_self_assessment(self, pk):
        try:
            return AssessmentModel.objects.filter(person_assessed=pk).order_by('-created_at')
        except Strands.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        self.validate_access(request, pk)
        assessments = self.get_self_assessment(pk)
        serializers = AssessmentSerializer(assessments, many= True)
        return Response(serializers.data)

class AssesserAssessment(APIView):
    permission_classes = (IsAuthenticated,)

    def get_assesser_assessment(self, pk):
        try:
            return AssessmentModel.objects.filter(person_assessing=pk).order_by('-created_at')
        except Strands.DoesNotExist:
            raise Http404()
    
    def get(self, request, pk, format=None):
        this_user = User.objects.get(pk=pk)
        if this_user == request.user:
            pass
        elif request.user.is_supervisor:
            pass
        else:
            raise Http404()
        assessments = self.get_assesser_assessment(pk)
        serializers = AssessmentSerializer(assessments, many= True)
        return Response(serializers.data)

class CompetencyStrands(APIView):

    def get(self, request, id, format=None):
        strands = Strands.objects.filter(competency = id)
        serializers = StrandsSerializer(strands, many=True)
        return Response(serializers.data)

class GetAssesserAssesseeAverage(APIView):

    def get_average(self ,pk , id1, id):
        values = AssessmentModel.objects.filter(competency = pk,person_assessed = id1, person_assessing = id).values_list('value', flat = True)
        sum_num = 0
        asses = 0

        if len(values) >= 1:
            for value in values:
                sum_num = sum_num + value

            average = sum_num / len(values)
            return average

        else:
            return asses


    def get(self, request,pk , id1, id, format=None):
        averages = self.get_average(pk , id1, id)
        return Response(averages)


class GetAssesseeAverage(APIView):

    def get_average(self ,pk , id):
        values = AssessmentModel.objects.filter(competency = pk, person_assessed = id, person_assessing = id).values_list('value', flat = True)
        sum_num = 0
        asses = 0

        if len(values) >= 1:
            for value in values:
                sum_num = sum_num + value

            average = sum_num / len(values)
            return average

        else:
            return asses


    def get(self, request,pk, id, format=None):
        average = self.get_average(pk,id)
        return Response(average)
