from django.urls import path
from . import views

urlpatterns = [
    path('vehicle-view/', views.VehicleView.as_view()),
]