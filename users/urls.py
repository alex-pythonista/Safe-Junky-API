from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify'),
    ]