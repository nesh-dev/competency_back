from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistrationSerializer,LoginSerializer,EmailSerializer,PasswordUpdateSerializer
from rest_framework import status 
from rest_framework.response  import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.template.loader import render_to_string
from .helper.email_helper import send_email 
from django.conf import settings 
from .jwt import get_token_data
from .models import User
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
        data = serializer.data
        domain = "http://" + request.get_host() + "/api/v1/verify/{}"
        url = domain.format(str(data['token']))
        body = render_to_string('activation-email.html', {
            'link': url,
            'user_name': data["user_name"]
        })
        subject = 'Verify your email'
        message = 'Please verify your account.'
        # send email to the user for verification
        send_email(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[data["email"]],
            html_message=body,
            fail_silently=False,)
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

class VerifyAPIView(generics.RetrieveAPIView):
    """
    A class to verify user using the token sent to the email
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    @classmethod
    def get(self, request, token):
        """
        Overide the default get method
        """
        user = get_token_data(token)
        user.is_active = True
        user.save()
        return Response(data={"message":"User Account  Activated Succesfully "},
                        status=status.HTTP_200_OK)  

class SendPasswordResetLinkAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request):
        """
        here, the user provides email to be used to get a link. The email must be registered,
        token gets generated and sent to users via link.
        """
        email = request.data.get('email', {})
        serializer = self.serializer_class(data={'email':email})
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = {"message":"The email provided is not registered"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        token = user.token
        domain = settings.PASSWORD_RESET_URL
        url = domain.format(str(token))
        body = render_to_string('password_reset.html', {
            'link': url,
            'user_name': user.user_name
        })
        subject = 'reset your password'
        message = 'Please reset your password.'
        # send email to the user for verification
        send_email(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user.email],
            html_message=body,
            fail_silently=False,)

        return_message = {'message':"Check up your email for password reset link",
                          }
        return Response(return_message, status=status.HTTP_200_OK)

class PasswordUpdateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordUpdateSerializer
    def patch(self, request):
        """
        Here, the user has received an email with a link to reset password.
        The user provides a new password.
        Token gets verified against the user.
        Once all checks have passed, the new password gets saved.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate_password_(request.data)
        password = request.data.get('password', {})
        user.set_password(password)
        user.save() 

        return_message = {'message':"Password updated successfully",
                          }
        return Response(return_message, status=status.HTTP_200_OK)
               

    

