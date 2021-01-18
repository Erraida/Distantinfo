# Generated by Django 3.1.4 on 2021-01-13 14:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_favorite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Закладка', 'verbose_name_plural': 'Закладки'},
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('User', 'Lecture')},
        ),
    ]