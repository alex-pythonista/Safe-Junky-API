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

    def create(self, validated_data):
        vehicle_models_data = validated_data.pop('vehicle_models', [])
        vehicle_brand = models.VehicleBrand.objects.create(**validated_data)

        for vehicle_model_data in vehicle_models_data:
            models.VehicleModel.objects.create(brand=vehicle_brand, **vehicle_model_data)

        return vehicle_brand



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

    def create(self, validated_data):
        vehicle_brand_data = validated_data.pop('vehicle_brand')
        vehicle_brand_serializer = VerhicleBrandSerializer(data=vehicle_brand_data)
        vehicle_brand_serializer.is_valid(raise_exception=True)
        vehicle_brand = vehicle_brand_serializer.save()

        vehicle = models.Vehicle.objects.create(vehicle_brand=vehicle_brand, **validated_data)
        return vehicle
  
        
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