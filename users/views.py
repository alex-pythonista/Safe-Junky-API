from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from . import serializers, models
from utils.azure_email_service import send_email

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
                send_email(to=user.email, otp=generated_otp)
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
                        'token': token.key
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
        