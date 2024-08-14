from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.validators import YouTubeLinkOnlyValidator

from materials import models
from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkOnlyValidator(fields=['name', 'description', 'link_to_video'])]


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        return obj.subscription.filter(user=self.context.get('request').user).exists()

    def get_count_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'image', 'count_lesson_in_course', 'lesson', "subscription",)
        validators = [YouTubeLinkOnlyValidator(fields=['name', 'description'])]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    method = serializers.CharField(default=serializers.CreateOnlyDefault('TRAN'))

    class Meta:
        model = models.Payment
        fields = '__all__'

