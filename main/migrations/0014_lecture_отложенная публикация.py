# Generated by Django 3.1.4 on 2021-04-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210404_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='Отложенная публикация',
            field=models.BooleanField(default=None),
        ),
    ]
