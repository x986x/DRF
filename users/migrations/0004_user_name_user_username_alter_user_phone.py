# Generated by Django 5.0.6 on 2024-07-15 12:14

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_delete_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(
                default="", max_length=80, unique=True, verbose_name="Имя"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                default=123,
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Укажите телефон",
                max_length=35,
                null=True,
                verbose_name="Телефон",
            ),
        ),
    ]
