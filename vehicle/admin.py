from django.contrib import admin
from . import models
from . models import Vehicle
# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'vehicle_brand',)
    search_fields = ()
    list_per_page = 25


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(models.VehicleBrand)
admin.site.register(models.VehicleModel)