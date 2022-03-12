from django.urls import path 
from .views import MyTokenObtainPairView, get_user, get_all_users, register_user
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'users'

urlpatterns = [
    path('login/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', get_user, name='get_user_profile'),
    path('users/', get_all_users, name='get_all_users'),
    path('register/', register_user, name='register-user'),
]