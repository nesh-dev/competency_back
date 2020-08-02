from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework import status 
from rest_framework.response  import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model as user_model
User = user_model()
from apps.supervisor.models import Department
from apps.manager.models import ManagerProfile
from apps.reportee.models import ReporteeProfile

# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer
    def post(self, request):
        """
        Handle user Signup
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.validate_password_(user)
        serializer.save()

        if_reportee = serializer.validated_data['is_reportee']        
        if if_reportee:
            uname = serializer.validated_data['user_name']
            this_user = User.objects.get(user_name = uname)
            reportee_profile = ReporteeProfile.objects.get(user = this_user)
            current_manager = request.user
            manager_profile = ManagerProfile.objects.get(user = current_manager)
            manager_dept = Department.objects.get(manager = manager_profile)
            reportee_profile.department = manager_dept
            reportee_profile.save()



        data = serializer.data
        return_message = {'message':"Signup Successful",
                          'user': data}
        return Response(return_message, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.CreateAPIView):
    # Login user class
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        """
        Handle user signup
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        

    

