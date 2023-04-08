from django.contrib import admin
from . import models
from . models import Vehicle
# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'vehicle_brand', 'vehicle_image_preview')
    search_fields = ()
    list_per_page = 25

    def vehicle_image_preview(self, obj):
        return obj.vehicle_image_preview()
    
    vehicle_image_preview.allow_tags = True
    vehicle_image_preview.short_description = 'Vehicle Image'

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(models.VehicleBrand)
admin.site.register(models.VehicleModel)
admin.site.register(models.DrivingLicense)