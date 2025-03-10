from django.urls import path
from .views import (
    RegisterView, VerifyTokenView, CustomTokenObtainPairView, 
    UserDetailView, AdminOnlyView, ManagerView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    path("verify-token/", VerifyTokenView.as_view(), name="verify-token"),
    
    # Role-based APIs
    path("admin/", AdminOnlyView.as_view(), name="admin-view"),
    path("manager/", ManagerView.as_view(), name="manager-view"),
]
