from django.contrib.auth import get_user_model
from django.db import models


METHOD_CHOISES = [
    ('CASH', 'оплата наличными'),
    ('TRAN', 'перевод на счет')
]

User = get_user_model()

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    Модель курса, содержит поля: название,превью (картинка), описание
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(
        max_length=120, verbose_name="Название куса", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="materials/course/image",
        **NULLABLE,
        verbose_name="Изображение",
        help_text="Добавьте изображение"
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание курса", help_text="Укажите описание курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """
    Модель урока, содержит поля: название, курс, описание, превью (картинка), ссылка на видео
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(
        max_length=150, verbose_name="Урок", help_text="Укажите название урока"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="Курс", help_text="Выберите курс", related_name="lesson"
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    image = models.ImageField(
        upload_to="materials/lesson/image",
        **NULLABLE,
        verbose_name="Изображение",
        help_text="Добавьте изображение"
    )
    link_to_video = models.CharField(
        max_length=150,
        **NULLABLE,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_of_pay = models.DateField(auto_now=True, verbose_name='дата оплаты')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=4, choices=METHOD_CHOISES)
    filterset_fields = ['category', 'in_stock']
    session_id = models.TextField(verbose_name='id сессии', **NULLABLE)
    payment_link = models.TextField(verbose_name='ссылка на оплату', **NULLABLE)


    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='unique_subscription')
        ]
