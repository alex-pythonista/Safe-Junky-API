from . import emergency_view, views
from django.urls import path

urlpatterns = [
    # User Information
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('delete-account/', views.delete_account, name='delete-profile'),

    # Emergency Information
    path('emergency-info/', views.EmergencyInfoView.as_view(), name='emergency-info'),
    path('add-blood-group/', emergency_view.create_blood_group, name='add-blood-group'),
    path('update-blood-group/', emergency_view.update_blood_group, name='update-blood-group'),
    
    # Contact Information
    path('view-contacts/', emergency_view.get_contacts, name='add-contact'),
    path('create-contact/', emergency_view.create_contact, name='create-contact'),
    path('update-contact/<int:id>', emergency_view.update_contact, name='update-contact'),
    ]