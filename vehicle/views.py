from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from . import serializers, models


# Create your views here.

class VehicleView(views.APIView):
    serializer_class = serializers.VehicleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            vehicle_obj = models.Vehicle.objects.filter(user=request.user)
            serializer = self.serializer_class(vehicle_obj, many=True)
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
