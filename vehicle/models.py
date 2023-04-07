from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=30, unique=True)
    vehicle_image = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    vehicle_brand = models.ForeignKey('VehicleBrand', on_delete=models.CASCADE, related_name='vehicle_brands')

    def __str__(self):
        return f"{self.user.full_name} - {self.registration_number}"
    
    
class VehicleBrand(models.Model):
    
    VEHICLE_TYPE = (
        ('Bike | Scooter', 'Bike | Scooter'),
        ('Car | Jeep', 'Car | Jeep'),
        ('Bus | Van', 'Bus | Van'),
        ('Auto rickshaw', 'Auto rickshaw'),
        ('Truck', 'Truck'),
    )

    brand_name = models.CharField(max_length=30)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)

    def __str__(self):
        return f"{self.brand_name} - {self.vehicle_type}"


class VehicleModel(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='vehicle_models')
    model_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.brand.brand_name} - {self.model_name}"
        