# Generated by Django 5.0.6 on 2024-07-11 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                blank=True,
                help_text="Выберите курс",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lesson",
                to="materials.course",
                verbose_name="Курс",
            ),
        ),
    ]
