from django.contrib.auth.hashers import make_password
from django_filters import rest_framework
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from users import models, serializers


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        raw_password = serializer.validated_data.get('password')
        password = make_password(raw_password)
        serializer.save(password=password)


class UserListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]
