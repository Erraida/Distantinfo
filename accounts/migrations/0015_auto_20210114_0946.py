# Generated by Django 3.1.4 on 2021-01-14 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0014_auto_20210114_0921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestrole',
            options={'verbose_name': 'Запрос роли', 'verbose_name_plural': 'Запросы роли'},
        ),
        migrations.AlterModelOptions(
            name='useraccount',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=1000, verbose_name='Заметка')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Закладка',
                'verbose_name_plural': 'Закладки',
            },
        ),
    ]