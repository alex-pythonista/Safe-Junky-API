from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

from django.shortcuts import get_object_or_404
from django.conf import settings

import os
from . import serializers, models


# Create your views here.

class VehicleView(views.APIView):
    serializer_class = serializers.VehicleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        try:
            if pk is not None:
                vehicle_obj = models.Vehicle.objects.filter(pk=pk, user=request.user).first()
                if vehicle_obj is None:
                    return Response({'error': 'Vehicle not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                vehicle_obj = models.Vehicle.objects.filter(user=request.user).order_by('-created_at')
            serializer = self.serializer_class(vehicle_obj, many=not pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            serializers = self.serializer_class(data=request.data)
            if serializers.is_valid():
                serializers.save(user=request.user)
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            vehicle_obj = models.Vehicle.objects.filter(pk=pk, user=request.user).exists()
            if vehicle_obj is False:
                return Response({'error': 'Vehicle not found'}, status=status.HTTP_400_BAD_REQUEST)
            models.Vehicle.objects.filter(pk=pk, user=request.user).delete()
            return Response({'message': 'Vehicle deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

class AddVehicleView(views.APIView):
    serializer_class = serializers.AddVehicleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            registration_number = serializer.validated_data.get('registration_number')
            vehicle_image = serializer.validated_data.get('vehicle_image')
            vehicle_brand = serializer.validated_data.get('vehicle_brand')
            vehicle_model = serializer.validated_data.get('vehicle_model')
            vehicle_type = serializer.validated_data.get('vehicle_type')

            
            vehicle_brand = get_object_or_404(models.VehicleBrand, brand_name=vehicle_brand, vehicle_type=vehicle_type)
            vehicle_model = get_object_or_404(models.VehicleModel, brand=vehicle_brand.id, model_name=vehicle_model)

            # check registration number already exists or not
            if models.Vehicle.objects.filter(registration_number=registration_number).exists():
                return Response({'error': 'Registration number already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                vehicle_obj = models.Vehicle.objects.create(
                user=user,
                registration_number=registration_number,
                vehicle_image=vehicle_image,
                vehicle_brand=vehicle_brand,
                vehicle_model=vehicle_model
                )
                vehicle_obj.save()
                return Response({'success': 'Vehicle added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_all_brands(request):
    try:
        brand_obj = models.VehicleBrand.objects.filter(vehicle_type=request.query_params.get('vehicle_type'))
        serializer = serializers.BrandSerializer(brand_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetModelsByBrands(views.APIView):
    serializer_class =  serializers.ModelSerializerBasedOnBrands
    search_fields = ['brand__brand_name', 'brand__vehicle_type']

    def get(self, request):
        try:
            brand_name = request.GET.get('brand_name')
            vehicle_type = request.GET.get('vehicle_type')
            queryset = models.VehicleModel.objects.filter(brand__brand_name=brand_name, brand__vehicle_type=vehicle_type)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VehicleDrivingLicense(views.APIView):
    serializer_class = serializers.DrivingLicenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            driving_license_obj = models.DrivingLicense.objects.filter(user=request.user).first()
            if driving_license_obj is None:
                return Response({'error': 'Driving license not found'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(driving_license_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if models.DrivingLicense.objects.filter(user=request.user).exists():
                    return Response({'error': 'Driving license already exists'}, status=status.HTTP_400_BAD_REQUEST)
                license_file = serializer.validated_data.get('license_file')
                driving_license_obj = models.DrivingLicense.objects.create(
                    user=request.user,
                    license_file=license_file
                )
                driving_license_obj.save()
                return Response({'success': 'Driving license added successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            driving_license_obj = models.DrivingLicense.objects.filter(user=request.user).first()
            if driving_license_obj:
                file_path = os.path.join(settings.MEDIA_ROOT, str(driving_license_obj.license_file))
                os.remove(file_path)
                driving_license_obj.delete()
                return Response({'success': 'Driving license deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No driving license found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class RegistrationSearchView(views.APIView):
    serializer_class = serializers.VehicleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            registration_number = request.query_params.get('registration_number')           
            vehicle_obj = models.Vehicle.objects.filter(registration_number__iexact=registration_number).first()
            if vehicle_obj:
                serializer = self.serializer_class(vehicle_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No vehicle found with this registration number'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)