# users/urls.py
from django.urls import path
from .views import RegisterView, UserListView, ProfileView, UserDetailView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('me/', ProfileView.as_view(), name='user-profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair_custom'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:username>/', UserDetailView.as_view(), name='user-detail'),
]
