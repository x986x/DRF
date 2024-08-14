from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials import models, serializers
from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination, LessonPagination
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from materials.services import create_product, create_price, create_session
from users.permissions import IsModerator, UserListOnly, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet-класс для вывода списка курсов.
    """
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsModerator | UserListOnly]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsOwner | IsModerator]
        return [permission() for permission in [IsAuthenticated] + self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение списка сущностей.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | UserListOnly]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Базовый класс Generic-классов, отвечающий за отображение одной сущности."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ['method', 'lesson', 'course']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, method='TRAN')

        if payment.course is None:
            raise ValueError("Курс, связанный с оплатой, отсутствует. Невозможно создать продукт.")

        product = create_product(payment.course)
        price = create_price(product=product, amount=payment.amount)

        # Передаем только price
        session_id, session_url = create_session(price)

        payment.session_id = session_id
        payment.payment_link = session_url
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()


class SubscriptionAPIView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="response message, can contain \"subscribed\" or \"unsubscribed\"",
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="string of response message",
                    example="subscribed"
                )
            }

        )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, description='course for altering subscription status',
            properties={
                'course': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='course for subscription / unsubscription id',
                    example="1"
                ),
            }
        ),

    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course.objects.filter(pk=self.request.data.get('course')))
        subscription_data = {
            'user': user,
            'course': course
        }
        is_subscribed = Subscription.objects.filter(**subscription_data).exists()
        if is_subscribed:
            Subscription.objects.filter(**subscription_data).delete()
            message = 'unsubscribed'
        else:
            Subscription.objects.create(**subscription_data)
            message = 'subscribed'
        return Response({'message': message})
