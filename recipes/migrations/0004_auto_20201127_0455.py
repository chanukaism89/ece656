# Generated by Django 3.1.2 on 2020-11-27 04:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20201125_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='recipe_submitted_date',
            field=models.DateField(default=datetime.date(2020, 11, 27)),
        ),
    ]
