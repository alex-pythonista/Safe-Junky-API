from django.urls import path
from . import views

urlpatterns = [
    path('add-vehicle/', views.VehicleView.as_view()),
]