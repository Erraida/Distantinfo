# Generated by Django 3.1.4 on 2021-01-19 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210114_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='Group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.group'),
        ),
    ]
