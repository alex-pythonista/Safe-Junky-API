from django.urls import path
from . import views

urlpatterns = [
    path('vehicle-view/', views.VehicleView.as_view()),
    path('get-all-brands/', views.get_all_brands),
]