from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from . import serializers, models
from users.tasks import send_email_task
import random

# Create your views here.

class UserRegisterView(generics.GenericAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                generated_otp = random.randint(1000, 9999)
                send_email_task.delay(user.email, generated_otp)
                models.Otp.objects.create(user=user, otp=generated_otp)
                if user is not None:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'message': 'User created successfully! Please check you email for OTP verification!'
                    }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                user = authenticate(email=email, password=password)
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'full_name' : user.full_name,
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = serializers.VerifyOtpSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                otp = serializer.data.get('otp')
                user = models.User.objects.get(id=request.user.id)
                otp_obj = models.Otp.objects.get(user=user)
                if otp_obj is not None:
                    generated_otp = otp_obj.otp
                    if int(generated_otp) == int(otp):
                        otp_obj.has_used = True
                        user.verified = True
                        user.save()
                        otp_obj.save()
                        token = Token.objects.get_or_create(user=user)
                        return Response({
                            'message': 'OTP verified successfully',
                            'token': token[0].key,
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'message': 'Invalid OTP',
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'message': 'Invalid phone number',
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e),
                'message' : 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class RequestOtpForPasswordResetView(generics.GenericAPIView): 
    permission_classes = [AllowAny]
    serializer_class = serializers.RequestOtpForPasswordResetSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                user = models.User.objects.get(email=email)
                if user is not None:
                    user.verified = False
                    user.save()

                    generated_otp = random.randint(1000, 9999)
                    send_email_task.delay(email, generated_otp)
                    models.Otp.objects.create(user=user, otp=generated_otp, has_used=False)
                    return Response({
                        'message': 'OTP sent successfully! Please check your email'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'User not found'
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordOTPVerifyView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordOtpVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                otp = serializer.validated_data.get('otp')
                user_obj = models.User.objects.get(email=email)
                otp_obj = models.Otp.objects.get(user=user_obj, otp=otp)
                if otp_obj is not None:
                    otp_obj.has_used = True
                    otp_obj.save()
                    return Response({
                        'message': 'OTP verified successfully! Please set your new password'
                    }, status=status.HTTP_200_OK)   
                return Response({
                    'error': 'Invalid OTP'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user_obj = models.User.objects.get(email=email)
                verification_status = user_obj.verified
                if verification_status is False:
                    user_obj.set_password(password)
                    user_obj.verified = True
                    user_obj.save()
                    return Response({
                        'message': 'Password changed successfully'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Request for new OTP and try again!'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = models.User.objects.get(id=request.user.id)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class EmergencyInfoView(generics.GenericAPIView):
    serializer_class = serializers.EmergencyInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

        
    def get(self, request):
        try:
            emergency_info = models.EmergencyInformation.objects.get(user=request.user)
            serializer = self.serializer_class(emergency_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    try:
        user = models.User.objects.get(id=request.user.id)
        user.delete()
        return Response({
            'message': 'Account deleted successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)