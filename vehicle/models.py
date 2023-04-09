from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from users.models import BaseModel

User = get_user_model()

# Create your models here.
class Vehicle(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=30, unique=True)
    vehicle_image = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    vehicle_brand = models.ForeignKey('VehicleBrand', on_delete=models.CASCADE, related_name='vehicle_brands')
    vehicle_model = models.ForeignKey('VehicleModel', on_delete=models.CASCADE, related_name='vehicle_models', null=False, blank=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.registration_number}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Vehicle.objects.get(pk=self.pk)
            if old_instance.vehicle_image and self.vehicle_image != old_instance.vehicle_image:
                old_instance.vehicle_image.delete(save=False)
            if old_instance.vehicle_image and self.vehicle_image != old_instance.vehicle_image:
                old_instance.vehicle_image.delete(save=False)
        super(Vehicle, self).save(*args, **kwargs)

    def vehicle_image_preview(self):
        if self.vehicle_image:
            return format_html('<img src="{}" height="100"/>'.format(self.vehicle_image.url))

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
        

class DrivingLicense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driving_license')
    license_file = models.FileField(upload_to='driving_license')

    def __str__(self):
        return f"{self.user.full_name}'s Driving License"

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = DrivingLicense.objects.get(pk=self.pk)
            if old_instance.license_file and self.license_file != old_instance.license_file:
                old_instance.license_file.delete(save=False)
        super(DrivingLicense, self).save(*args, **kwargs)


       