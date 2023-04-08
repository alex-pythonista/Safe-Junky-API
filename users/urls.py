from . import views
from django.urls import path

urlpatterns = [
    # Authentication
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    # Emergency Information
    path('emergency-info/', views.EmergencyInfoView.as_view(), name='emergency-info'),
    path('add-blood-group/', views.create_blood_group, name='add-blood-group'),
    path('update-blood-group/', views.update_blood_group, name='update-blood-group'),
    ]