from django.urls import path
from .views import *

app_name='accounting'
urlpatterns = [
    path('register/',UserRegisterationView.as_view(),name='register'),
    path('verify_registeration/',VerifyRegisterationView.as_view(),name='verify_registeration'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('user_panel/',UserPanelView.as_view(),name='user_panel'),
    path('password_change/',PasswordChangeView.as_view(),name='password_change'),
    path('forget_password/',ForgetPasswordView.as_view(),name='forget_password'),
]
