from user.views import CreateUserView
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, 
TokenRefreshView, TokenVerifyView)


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', CreateUserView.as_view(), name='register'),
    # path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify', TokenVerifyView.as_view(), name='token_verify'),
]