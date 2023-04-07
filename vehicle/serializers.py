from rest_framework import serializers
from . import models


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleModel
        fields = [
            'model_name',
        ]


class VerhicleBrandSerializer(serializers.ModelSerializer):
    vehicle_models = BrandModelSerializer(many=True)
    class Meta:
        model = models.VehicleBrand
        fields = [
            'brand_name',
            'vehicle_type',
            'vehicle_models',
        ]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_brand = VerhicleBrandSerializer()
    
    class Meta:
        model = models.Vehicle
        fields = [
            'id',
            'user',
            'registration_number',
            'vehicle_image',
            'vehicle_brand',
        ]

class AddVehicleSerializer(serializers.Serializer):
    registration_number = serializers.CharField(required=True)
    vehicle_image = serializers.ImageField(required=False, allow_null=True)
    vehicle_brand = serializers.CharField(required=True)
    vehicle_model = serializers.CharField(required=True)
    vehicle_type = serializers.CharField(required=True)


        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleBrand
        fields = [
            'brand_name',
            'vehicle_type',
        ]

class ModelSerializerBasedOnBrands(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleModel
        fields = [
            'model_name',
        ]