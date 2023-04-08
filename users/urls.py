from . import emergency, views
from django.urls import path

urlpatterns = [
    # Authentication
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    # Emergency Information
    path('emergency-info/', views.EmergencyInfoView.as_view(), name='emergency-info'),
    path('add-blood-group/', emergency.create_blood_group, name='add-blood-group'),
    path('update-blood-group/', emergency.update_blood_group, name='update-blood-group'),
    
    path('view-contacts/', emergency.get_contacts, name='add-contact'),
    path('update-contact/', emergency.update_contact, name='update-contact'),
    
    ]