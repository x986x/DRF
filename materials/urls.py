from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionAPIView, PaymentCreateAPIView, \
    PaymentRetrieveAPIView
from materials.apps import MaterialsConfig


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons-retrieve'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons-create'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons-delete'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons-update'),
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
    path('payment-create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment-retrieve/', PaymentRetrieveAPIView.as_view(), name='payment-retrieve'),
] + router.urls
