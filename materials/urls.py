from django.urls import path, include
from rest_framework.routers import DefaultRouter

from materials.views import (CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView,
                             LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView)
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
] + router.urls
