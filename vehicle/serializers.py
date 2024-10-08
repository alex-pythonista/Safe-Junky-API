from rest_framework import serializers
from . import models

class VerhicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleBrand
        fields = [
            'brand_name',
            'vehicle_type',
        ]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_brand = VerhicleBrandSerializer()
    model_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Vehicle
        fields = [
            'id',
            'registration_number',
            'vehicle_image',
            'vehicle_brand',
            'model_name',
        ]
    
    def get_model_name(self, obj):
        return obj.vehicle_model.model_name

        
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


class AddVehicleSerializer(serializers.Serializer):
    registration_number = serializers.CharField(required=True)
    vehicle_image = serializers.ImageField(required=False, allow_null=True)
    vehicle_brand = serializers.CharField(required=True)
    vehicle_model = serializers.CharField(required=True)
    vehicle_type = serializers.CharField(required=True)

class DrivingLicenseSerializer(serializers.Serializer):
    license_file = serializers.FileField(required=True)
    fileds = [
        'license_file',
    ]