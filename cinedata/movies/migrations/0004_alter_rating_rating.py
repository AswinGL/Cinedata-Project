# Generated by Django 5.2.3 on 2025-06-23 04:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
