from django.urls import path

from . import views

urlpatterns = [

    path('login/', views.LoginView.as_view()),

    path('user-registration/',views.UserRegistrationView.as_view()),

    path('otp-verify/',views.OTPVerifyView.as_view()),

    path('otp-regenerate/',views.OTPRegenerationView.as_view()),

]