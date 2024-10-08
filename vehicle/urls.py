from django.urls import path
from . import views

urlpatterns = [
    path('vehicle-info/<int:pk>', views.VehicleView.as_view()),
    path('vehicle-info/', views.VehicleView.as_view()),
    path('add-vehicle/', views.AddVehicleView.as_view()),
    path('delete-vehicle/<int:pk>', views.VehicleView.as_view()),
    
    path('get-all-brands/', views.get_all_brands),
    path('get-models-by-brands/', views.GetModelsByBrands.as_view()),

    path('driving-license/', views.VehicleDrivingLicense.as_view()),

    path('search-vehicle/', views.RegistrationSearchView.as_view()),
]