from django.urls import path, include
from .views import RegistrationAPIView,LoginAPIView,VerifyAPIView,SendPasswordResetLinkAPIView,PasswordUpdateAPIView

urlpatterns = [

  path('signup/', RegistrationAPIView.as_view(), name='user-registration'),
  path('login/', LoginAPIView.as_view(), name='user-login'),
  path('verify/<str:token>', VerifyAPIView.as_view(), name='verify_account'),
  path('send_email/', SendPasswordResetLinkAPIView.as_view(), name='password_reset_email'),
  path('password_update/', PasswordUpdateAPIView.as_view(), name='password_update'),

  
]
