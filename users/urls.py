from django.urls import path
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('retrieve/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('destroy/', UserDestroyAPIView.as_view(), name='user-destroy'),
    path('obtain/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
